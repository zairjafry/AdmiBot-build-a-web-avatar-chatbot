# talk_with_any_file_langchain.py

# !pip install langchain langchain_community huggingface_hub sentence_transformers faiss-cpu unstructured chromadb Cython tiktoken unstructured[local-inference] -q

import getpass
import os
import textwrap
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import HuggingFaceHub
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate  # Updated import path

import keyboard

def set_huggingfacehub_token():
    if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = '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' # getpass.getpass("Provide your HUGGINGFACEHUB TOKEN")

def wrap_text_preserve_newlines(text, width=110):
    lines = text.split('\n')
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = '\n'.join(wrapped_lines)
    return wrapped_text

def load_documents(filepath):
    loader = TextLoader(filepath)
    documents = loader.load()
    return documents

def split_documents(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    return docs

def save_db(db, filename):
    FAISS.write_index(db, filename)

def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local('AdmiBotVectorIndex')
    return db

def create_qa_chain(db):
    template = """
    <s>[INST] You're a University Representative. Use the following context and the chat history to answer the question, Please respond with no more than 10 tokens:

    Context:
    <ctx>
    {context}
    </ctx>

    Chat History:
    <hs>
    {history}
    </hs>

    Question:
    {question}

    Please respond with no more than 1 lines based on the given information without providing explanations.
    - If the user greets, respond accordingly.
    - If you don't have any context, apologize accordingly.
    - If the question is not directly related to the context provided, answer "I am sorry, I don't know" and do not answer further. End the answer right there.
    - Do not provide any information if the question is outside the context.
    - Do not provide any information Adult Websites or unscensored content.
    [/INST]
    """
    prompt = PromptTemplate(
        input_variables=["history", "context", "question"],
        template=template,
    )
    memory = ConversationBufferMemory(
        memory_key="history",
        input_key="question"
    )
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mistral-7B-Instruct-v0.2", 
        temperature=0.1, 
        max_length=1024
    )
    chain = RetrievalQA.from_chain_type(
        llm,
        chain_type='stuff',
        retriever=db.as_retriever(),
        chain_type_kwargs={
            "prompt": prompt,
            "memory": memory
        }
    )
    return chain

def get_user_query():
    query = input("You: ")
    return query

def search_similar_documents(db, query):
    docs = db.similarity_search(query)
    return docs

def run_qa_chain(chain, docs, query):
    output = chain.run(query)
    return output

def play_output(output):
    print(f"AI: {output}")

def conversation(chain, db):
    print("Start talking to the bot. Type 'e' to exit.")
    while True:
        query = get_user_query()
        if query.lower() == 'e':
            print("Exiting conversation.")
            break
        similar_docs = search_similar_documents(db, query)
        output = run_qa_chain(chain, similar_docs, query)
        play_output(output)

def get_or_create_db(filepath='dataset.txt'):
    set_huggingfacehub_token()
    embeddings = HuggingFaceEmbeddings()
    if os.path.exists("AdmiBotVectorIndex"):
        db = FAISS.load_local("AdmiBotVectorIndex", embeddings, allow_dangerous_deserialization=True)
    else:
        documents = load_documents(filepath)
        docs = split_documents(documents)
        db = create_vector_store(docs)
        db.save_local("AdmiBotVectorIndex")  # Save the newly created DB
    return db

# def main():
#     db = get_or_create_db()
#     chain = create_qa_chain(db)
#     conversation(chain, db)
#     print("....Exiting conversation...")

# if __name__ == "__main__":
#     main()

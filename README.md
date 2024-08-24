# AdmiBot: Build a Web Avatar Chatbot

## Project Description
A web-based project made using the Flask framework in Python. AdmiBot is a RAG-based chatbot created using LangChain and Hugging Face, developed in Python to serve as a university admin. It is integrated with NVIDIA Omniverse Audio2Face to facilitate natural conversations.

# Demo

![WhatsApp Image 2024-07-01 at 13 40 34_1297aa98](https://github.com/user-attachments/assets/8a6c3a57-7a9d-40c2-83f1-5103eb30d333)

***Video Demonstration on YouTube***

[![Video Demonstration on YouTube](https://img.youtube.com/vi/GnBqrS78ODk)](https://www.youtube.com/watch?v=GnBqrS78ODk)

# How It Works

![Admi-bot](https://github.com/user-attachments/assets/5ec4f3f7-5906-4d72-bc7a-cfab55522ea9)

### Audio Input

The user enters a query through a voice command, which gets converted into text format using Google's TTS API.

### RAG Chatbot Engine

The chat engine retrieves the context from the vector database, where all the embeddings are stored. After performing a similarity search, a context is generated and sent to Mistral 7B on Hugging Face along with the question. Finally, a response is generated and stored.

### Facial Animation Output

The stored text response is converted into audio using Google's TTS service and then sent to NVIDIA Audio2Face via gRPC protocol communication. The configured live streaming player plays the audio, resulting in real-time facial animation.

![image](https://github.com/user-attachments/assets/57b83159-ed8f-4178-9b8c-43c08136c2a9)

Omniverse Audio2Face is an application that brings avatars to life. With Omniverse Audio2Face, anyone can now create realistic facial expressions and emotions to match any voice-over track. The technology feeds the audio input into a pre-trained deep neural network developed by NVIDIA, and the network's output drives the facial animation of 3D characters in real-time.

# System Requirements

| Element           | Minimum Specifications                                               |
| ----------------- | -------------------------------------------------------------------- |
| **OS Supported**  | Windows 10 64-bit (Version 1909 and above)                           |
| **CPU**           | Intel i7, AMD Ryzen 2.5GHz or greater                                |
| **CPU Cores**     | 4 or higher                                                          |
| **RAM**           | 16 GB or higher                                                      |
| **Storage**       | 500 GB SSD or higher                                                 |
| **GPU**           | Any RTX GPU                                                          |

## Step-by-Step Guide to Deploy/Install AdmiBot

### Prerequisites

- **NVIDIA Audio2Face:** Ensure you have NVIDIA Audio2Face installed.
- **Character Selection:** Select a character such as Mark (male) or Claire (female) from the examples provided in Audio2Face.
- **Python and pip:** Ensure Python is installed on your system along with pip.

### Step-by-Step Installation

1. **Edit the Dataset:**
   - Before proceeding, you can edit the `dataset.txt` file to customize the information your chatbot will be aware of. Add any content you want the chatbot to know.
   - Be aware that altering the dataset may require you to change the prompt template declared in the `prompt` variable within the `AdmiBot_7b.py` file.

2. **Clone This Repository:**
   - Open your terminal or command prompt.
   - Navigate to the directory where you want to clone the repository.
   - Run the following command to clone the repository:
     ```bash
     git clone https://github.com/zairjafry/AdmiBot-build-a-web-avatar-chatbot.git
     ```
   - Navigate into the cloned directory:
     ```bash
     cd AdmiBot-build-a-web-avatar-chatbot
     ```

3. **Install Required Libraries/Packages:**
   - Ensure you are in the directory where the `requirements.txt` file is located.
   - Run the following command to install all necessary libraries/packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run NVIDIA Audio2Face:**
   - Open NVIDIA Audio2Face on your computer.
   - Select Mark from the 'Get Started' options.
   - Choose the audio player as the streaming player. If Mark is not available, you will need to manually attach the streaming player in the Action Graph by creating a streaming player.

5. **Configure WebRTC Streaming:**
   - Under the 'Extensions' tab in Audio2Face, install the WebRTC Client extension.
   - Enable the WebRTC Client extension and check the 'Autoload' option for future use.

6. **Run the Main Application:**
   - Run the `main.py` script:
     ```bash
     python main.py
     ```
   - After running the script, Flask will start a local server. The server address (e.g., `http://127.0.0.1:5000/`) will be provided in the terminal.
   - You can either click the link directly from the terminal or enter it into your web browser to access the chatbot interface.

## Creators
- **Syed Zair Hussain**
  - [GitHub](https://github.com/zairjafry)
  - [LinkedIn](https://www.linkedin.com/in/zairjafry)

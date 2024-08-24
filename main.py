from flask import Flask, render_template, request, jsonify, after_this_request
from AdmBot_tts import AudioRecorder, audio_to_text, play_audio  # Correct the import statement
import threading
import AdmiBot_7b
import random

db = AdmiBot_7b.get_or_create_db()
chain = AdmiBot_7b.create_qa_chain(db)
global_response = ''
app = Flask(__name__, static_folder='static')
recorder_thread = None
recorder = None

pause_responses = [
    "Hold on a moment...",
    "Just a second...",
    "Let me think about that...",
    "Please wait while I process your request...",
    "I'm working on that for you..."
]


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_page():
    return render_template('map.html')

@app.route('/pov')
def pov_page():
    return render_template('pov.html')

@app.route('/manual')
def manual_page():
    return render_template('manual.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recorder, recorder_thread
    input_filename = "input_audio.wav"
    recorder = AudioRecorder(input_filename)
    
    recorder_thread = threading.Thread(target=recorder.start_recording)
    recorder_thread.start()

    return jsonify({'status': 'success', 'message': 'I am Listening...'})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global recorder, recorder_thread
    if recorder_thread and recorder_thread.is_alive():
        recorder.stop_recording()
        recorder_thread.join()

        input_text = audio_to_text(recorder.filename)
        if(len(input_text.split())>10):
            pause_response = random.choice(pause_responses)
            play_audio(pause_response)

        if input_text.strip():  # Check if input_text is not empty or contains only whitespace
            response_text = chat(input_text)
            response_message = 'Processing what you said..'
        else:
            input_text = 'No Dialogue'
            response_text = "I am Sorry, I could not understand you"
            response_message = 'There was No Dialogue'
        
        response_json = jsonify({'status': 'success', 'message': response_message, 'query': input_text, 'response': response_text})

        @after_this_request
        def play_response_audio(response):
            def play_audio_thread():
                play_audio(response.get_json()['response'])

            audio_thread = threading.Thread(target=play_audio_thread)
            audio_thread.start()
            return response

        return response_json
    else:
        return jsonify({'status': 'failure', 'message': 'No recording in progress.'})


def chat(query):
    print("Query from stop_recording route:", query)
    similar_docs = AdmiBot_7b.search_similar_documents(db, query)
    response = AdmiBot_7b.run_qa_chain(chain, similar_docs, query)
    return response

if __name__ == '__main__':
    app.run(debug=True)

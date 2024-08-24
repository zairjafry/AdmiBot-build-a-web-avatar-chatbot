import pyaudio
import wave
import speech_recognition as sr
import pyttsx3
import threading
import keyboard
import grpc
import audio2face_pb2_grpc 
import audio2face_pb2
import wave
import pyaudio
import numpy as np
import soundfile
import sys
import time
from gtts import gTTS

def get_audio2face_client():
    channel = grpc.insecure_channel('localhost:50051')  # Change to your server address and port
    stub = audio2face_pb2_grpc.Audio2FaceStub(channel)
    return stub

def send_audio_stream(audio_file_path, player_name):
    url = 'localhost:50051'
    stub = get_audio2face_client()
    
    # Read audio file
    data, samplerate = soundfile.read(audio_file_path, dtype="float32")

    # Only Mono audio is supported
    if len(data.shape) > 1:
        data = np.average(data, axis=1)

    chunk_size = samplerate // 10  # Adjust the chunk size if needed
    sleep_between_chunks = 0.04  # Adjust the sleep duration if needed
    block_until_playback_is_finished = True

    with grpc.insecure_channel(url) as channel:
        stub = audio2face_pb2_grpc.Audio2FaceStub(channel)

        def make_generator():
            start_marker = audio2face_pb2.PushAudioRequestStart(
                samplerate=samplerate,
                instance_name=player_name,
                block_until_playback_is_finished=block_until_playback_is_finished,
            )
            # At first, we send a message with start_marker
            yield audio2face_pb2.PushAudioStreamRequest(start_marker=start_marker)
            # Then we send messages with audio_data
            for i in range(len(data) // chunk_size + 1):
                time.sleep(sleep_between_chunks)
                chunk = data[i * chunk_size : i * chunk_size + chunk_size]
                yield audio2face_pb2.PushAudioStreamRequest(audio_data=chunk.astype(np.float32).tobytes())

        request_generator = make_generator()
        print("Sending audio data...")
        response = stub.PushAudioStream(request_generator)
        if response.success:
            print("SUCCESS")
        else:
            print(f"ERROR: {response.message}")
    print("Closed channel")




class AudioRecorder:
    def __init__(self, filename):
        self.filename = filename
        self.CHUNK = 1024  # You can adjust this value
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100  # You can adjust this value
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.recording = False

    def start_recording(self):
        self.recording = True
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        print("Recording...")

        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def stop_recording(self):
        if self.recording:
            self.recording = False
            print("Finished recording.")
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

            wf = wave.open(self.filename, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()

def play_audio(text):
    engine = pyttsx3.init()
    voice=engine.getProperty('voices')
    engine.setProperty('voice',voice[1].id)
    engine.setProperty('rate', 135)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    #engine.say(text)
    engine.save_to_file(text, r'Audio_Response\output.wav')
    engine.runAndWait()
    
    # Setting up the Google TTS


    # tts = gTTS(text=text, lang='en-gb', tld='com' , slow=False)
    
    # # Save the speech to a file
    # output_file_path = r'Audio_Response\output.wav'
    # tts.save(output_file_path)

    audio_file_path = r'Audio_Response\output.wav'
    player_name = '/World/audio2face/PlayerStreaming'
    #/World/LazyGraph/PlayerStreaming
    send_audio_stream(audio_file_path, player_name)

def audio_to_text(filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Speech Recognition service; {e}")
        return ""

# if __name__ == "__main__":
#     input_filename = "input_audio.wav"  # Filename for recorded input audio

#     recorder = AudioRecorder(input_filename)

#     print("Press 'r' to start recording and 's' to stop recording.")

#     recording_thread = threading.Thread(target=recorder.start_recording)

#     while True:
#         if keyboard.is_pressed('r'):
#             if not recording_thread.is_alive():
#                 recording_thread = threading.Thread(target=recorder.start_recording)
#                 recording_thread.start()
#         elif keyboard.is_pressed('s'):
#             if recording_thread.is_alive():
#                 recorder.stop_recording()
#                 break

#     input_text = audio_to_text(input_filename)
#     print("Text from input audio:", input_text)

#     play_audio(input_text)



# # def Get_Speech():
#     input_filename = "input_audio.wav"  # Filename for recorded input audio
#     recorder = AudioRecorder(input_filename)

#     print("Click on the microphone to start recording and again to stop recording /n")

#     recording = False

#     def toggleRecording():
#         nonlocal recording
#         if not recording:
#             recording_thread = threading.Thread(target=recorder.start_recording)
#             recording_thread.start()
#             recording = True
#             showDialog('RECORDING STARTED!')
#         else:
#             recorder.stop_recording()
#             input_text = audio_to_text(input_filename)
#             play_audio(input_text)
#             showDialog('RECORDING STOPPED! Query: ' + input_text)
#             recording = False

#     document.getElementById('toggleButton').addEventListener('click', toggleRecording)

#     while True:
#         if keyboard.is_pressed('s'):
#             if recording:
#                 recorder.stop_recording()
#                 input_text = audio_to_text(input_filename)
#                 print("Text from input audio:", input_text)
#                 play_audio(input_text)
#                 showDialog('RECORDING STOPPED! Query: ' + input_text)
#                 recording = False
#                 break

#         elif keyboard.is_pressed('e'):
#             print("Exiting conversation.")
#             return 'Thankyou Goodbye!'

#     return input_text

import webrtcvad
import collections
import numpy as np
import pyaudio
import whisper

# --- VAD & Audio Configuration ---
VAD_AGGRESSIVENESS = 3      # 0 (least aggressive) to 3 (most aggressive)
SAMPLE_RATE = 16000         # Must be 8000, 16000, 32000, or 48000
FRAME_DURATION_MS = 30      # Duration of each audio frame in ms
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit audio

# --- Whisper Configuration ---
MODEL_TYPE = "base"
LANGUAGE = "en"

# --- Global State ---
model = None

def initialize_model():
    """Loads the Whisper model into memory."""
    global model
    if model is None:
        print(f"Loading Whisper model '{MODEL_TYPE}'...")
        model = whisper.load_model(MODEL_TYPE)
        print("Model loaded successfully.")

def transcribe_audio(audio_data):
    """Transcribes a byte buffer of audio data using the Whisper model."""
    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    result = model.transcribe(audio_np, language=LANGUAGE, fp16=False)
    return result['text'].strip()

def run_transcription(callback_function):
    """
    Main function to start listening and transcribing with VAD.
    """
    initialize_model()
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
    pa = pyaudio.PyAudio()

    stream = pa.open(format=pyaudio.paInt16,
                     channels=CHANNELS,
                     rate=SAMPLE_RATE,
                     input=True,
                     frames_per_buffer=FRAME_SIZE)

    print("\n--- AI Assistant is listening. Say 'exit' to quit. ---")
    
    while True:
        frames = collections.deque()
        is_speaking = False
        silence_counter = 0
        
        # --- Listen for speech ---
        print("LISTENING...")
        while True:
            audio_frame = stream.read(FRAME_SIZE)
            if vad.is_speech(audio_frame, SAMPLE_RATE):
                is_speaking = True
                print("Speaking detected, recording...", end='\r')
                frames.append(audio_frame)
                break
        
        # --- Record while speaking ---
        while is_speaking:
            audio_frame = stream.read(FRAME_SIZE)
            frames.append(audio_frame)
            if not vad.is_speech(audio_frame, SAMPLE_RATE):
                silence_counter += 1
                if silence_counter > 50:  # ~1.5 seconds of silence
                    is_speaking = False
                    print("\nSilence detected, processing...")
            else:
                silence_counter = 0
        
        # --- Transcribe the recorded speech ---
        recorded_audio = b"".join(list(frames))
        transcript = transcribe_audio(recorded_audio)
        
        if transcript:
            print("USER SAID:", transcript)
            if "exit" in transcript.lower():
                break
            # Call the main application logic with the transcribed text
            callback_function(transcript)

    # --- Cleanup ---
    stream.stop_stream()
    stream.close()
    pa.terminate()
    print("Transcription stopped.")

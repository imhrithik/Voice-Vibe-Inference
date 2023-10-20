import asyncio
import websockets
import io
import numpy as np
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Define the WebSocket server function to handle incoming audio data
async def audio_handler(websocket, path):
    # Receive audio data
    audio_data = await websocket.recv()
    print("audio rcved")

    # Process the audio data
    audio_bytes = io.BytesIO(audio_data)
    sample_rate = 44100  # Adjust as needed
    
    #here............
    audio_array = np.frombuffer(audio_bytes.read(), dtype=np.int16)

    # Save the audio to a file
    write("recorded_audio.wav", sample_rate, audio_array)
    print("Audio data received and saved.")

    # Generate and save the spectrogram
    plt.specgram(audio_array, Fs=sample_rate, cmap='viridis')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Spectrogram')
    
    # Save the spectrogram image in the 'spectrogram/' directory
    spectrogram_path = "spectrogram/spectrogram.png"
    plt.savefig(spectrogram_path)
    print("Spectrogram generated and saved.")

# Start the WebSocket server
start_server = websockets.serve(audio_handler, "0.0.0.0", 8765)  # Change the IP and port as needed
print("started")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

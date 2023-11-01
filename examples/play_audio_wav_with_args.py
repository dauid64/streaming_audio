import wave
import sys
import pyaudio

CHUNK = 1024

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

with wave.open(sys.argv[1], 'rb') as wf:
    # Instanciando o PyAudio, adquire os recursos do sistema para PortAudio
    p = pyaudio.PyAudio()

    # Abrindo e setando as informações do arquivo
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Reproduzindo o arquivo de áudio
    while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
        stream.write(data)

    # Fecha stream
    stream.close()

    # Libera recursos do sistema PortAudio
    p.terminate()

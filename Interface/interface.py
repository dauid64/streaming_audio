import tkinter as tk
import pyaudio
import wave

janela = tk.Tk()
janela.title = "Streaming de audio"
janela.configure(bg= "blue")

label = tk.Label(janela , text= "Olá!")
label.configure(bg = "blue", fg = "white")
label.pack()

iniciar_button = tk.Button(janela, text="Iniciar Transmissão")
iniciar_button.configure(bg = "blue", fg = "white")
iniciar_button.pack()

botao = tk.Button(janela, text="Pause")
botao.configure(bg = "black", fg= "white")
botao.pack()

status_label = tk.Label(janela, text="Aguardando início da transmissão...")
status_label.configure(bg = "blue", fg = "white")
status_label.pack()

janela.mainloop()

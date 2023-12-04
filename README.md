# Streaming de Áudio

![GitHub repo size](https://img.shields.io/github/repo-size/dauid64/streaming_audio?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/dauid64/streaming_audio?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/dauid64/streaming_audio?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/dauid64/streaming_audio?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/dauid64/streaming_audio?style=for-the-badge)

<p align="center">
    <img src="https://github.com/dauid64/streaming_audio/assets/94979678/2fd96c08-5096-450d-ba35-3ba28e4ca2fd" alt="Exemplo imagem">
</p>

> Este é um projeto para a disciplina de Redes de Computadores na UnB, com o objetivo de criar um sistema de streaming de áudio utilizando sockets.

### Requisitos

- [x] Cliente deve poder recuperar a lista de m´usicas no servidor
- [x] Cliente deve poder clicar para tocar uma m´usica hospedada no servidor
- [x] Se o cliente tentar tocar a m´usica e ela n˜ao estiver em cache local, buscar no servidor
- [x] O servidor deve transmitir a música em blocos de 5 segundos de ´audio
- [x] O cliente deve poder pausar a música, o que deve interromper a bufferiza¸c˜ao
- [x] Se o cliente retomar a execução do ponto parado ou reiniciar a m´usica, o buffer local deve ser
consumido
- [ ] Diferentes clientes devem ser capazes de se descobrir em uma rede local
- [ ] Clientes devem ser capazes de tocar a m´usica em um cliente remoto

## 💻 Pré-requisitos

Antes de começar, verifique se você atendeu aos seguintes requisitos:

- Você instalou a versão mais recente de `< Python >`
- Você tem uma máquina `<Windows / Linux / Mac>`

## 🚀 Instalando Streaming de Áudio

Para rodar o Streaming de Áudio é necessário instalar dependências de bibliotecas, siga então as seguintes etapas:

Linux e macOS:

```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Windows:

```
python -m venv venv
cd venv/Scripts
activate
pip install -r requirements.txt
```

## ☕ Usando Streaming de Áudio

Para usar o Streaming de Áudio, siga estas etapas:

. Primeiro execute o server
```
cd server
python app.py
```
. Depois execute o cliente em outro prompt
```
cd client
python app.py
```

Agora pode escolher as músicas que estão guardadas no servidor e ouvi-las!

## 🤝 Desenvolvedores

Às seguintes pessoas contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/dauid64" title="defina o titulo do link">
        <img src="https://github.com/dauid64/streaming_audio/assets/94979678/ca828726-8438-4c20-9227-b2639e13f96d" width="100px;" alt="Foto do Carlos David"/><br>
        <sub>
          <b>Carlos David</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/VitorDanelon" title="defina o titulo do link">
        <img src="https://github.com/dauid64/streaming_audio/assets/94979678/6cc31471-5f63-480f-81eb-b91e8bf44b83" width="100px;" alt="Foto do Vitor Danelon"/><br>
        <sub>
          <b>Vitor Danelon</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/raphaelCameloS" title="defina o titulo do link">
        <img src="https://github.com/dauid64/streaming_audio/assets/94979678/efd8131f-8bad-45fb-9441-6a333f5b7623" width="100px;" alt="Foto do Raphael Camelo"/><br>
        <sub>
          <b>Raphael Camelo</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

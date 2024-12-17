import datetime
import os
import random
import pyautogui
import webbrowser as wb
import pyjokes
from gtts import gTTS
import speech_recognition as sr
import pygame
import subprocess

# Inicializa o pygame para reproduzir áudio
pygame.mixer.init()

# Funções principais
def falar(texto):
    """Converte texto em fala e reproduz."""
    tts = gTTS(text=texto, lang='pt-br')
    tts.save("voz.mp3")
    pygame.mixer.music.load("voz.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def ouvir():
    """Captura o comando de voz do usuário e retorna como texto."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            comando = recognizer.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            falar("Desculpe, não entendi o que você disse.")
            return None
        except sr.RequestError:
            falar("O serviço de reconhecimento de fala não está disponível.")
            return None
        except Exception as e:
            falar(f"Ocorreu um erro: {e}")
            return None

def dizer_horas():
    """Informa as horas atuais."""
    hora_atual = datetime.datetime.now().strftime("%H:%M")
    falar(f"Agora são {hora_atual}.")
    print(f"Agora são {hora_atual}.")

def dizer_data():
    """Informa a data atual."""
    hoje = datetime.datetime.now()
    data_formatada = f"Hoje é dia {hoje.day} de {hoje.strftime('%B')} de {hoje.year}."
    falar(data_formatada)
    print(data_formatada)

def capturar_tela():
    """Captura uma screenshot e salva no diretório Imagens."""
    img = pyautogui.screenshot()
    caminho = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(caminho)
    falar("A captura de tela foi salva na sua pasta de imagens.")
    print(f"Screenshot salva em {caminho}.")

def tocar_musica(nome_musica=None):
    """Toca uma música da pasta Música no Linux."""
    pasta_musicas = os.path.expanduser("~/Músicas")  # Diretório padrão no Linux

    if not os.path.exists(pasta_musicas):
        falar("A pasta de músicas não foi encontrada.")
        return

    extensoes_validas = ('.mp3', '.wav', '.ogg')
    musicas = [musica for musica in os.listdir(pasta_musicas) if musica.endswith(extensoes_validas)]

    if nome_musica:
        musicas = [musica for musica in musicas if nome_musica.lower() in musica.lower()]

    if musicas:
        musica = random.choice(musicas)
        caminho_musica = os.path.join(pasta_musicas, musica)
        falar(f"Tocando {musica}.")
        print(f"Tocando {musica}.")
        subprocess.Popen(["xdg-open", caminho_musica])  # Abre com o player padrão no Linux
    else:
        falar("Nenhuma música encontrada.")
        print("Nenhuma música encontrada.")


def pesquisar_wikipedia(consulta):
    """Realiza uma busca no Wikipedia e retorna um resumo."""
    try:
        import wikipedia
        wikipedia.set_lang("pt")
        if not consulta:
            falar("Por favor, diga o que deseja pesquisar no Wikipédia.")
            return

        resultado = wikipedia.summary(consulta, sentences=2)
        falar(f"De acordo com a Wikipédia: {resultado}")
        print(resultado)
    except wikipedia.exceptions.DisambiguationError as e:
        falar("Encontrei muitos resultados. Por favor, seja mais específico.")
        print(e.options)
    except wikipedia.exceptions.PageError:
        falar("Não encontrei nada sobre isso na Wikipédia.")
    except Exception as e:
        falar("Ocorreu um erro ao acessar a Wikipédia.")
        print(e)


def contar_piada():
    """Conta uma piada em português."""
    piada = pyjokes.get_joke(language="pt")
    falar(piada)
    print(piada)

def saudar():
    """Saúda o usuário com base no horário atual."""
    hora = datetime.datetime.now().hour
    if 5 <= hora < 12:
        falar("Bom dia!")
    elif 12 <= hora < 18:
        falar("Boa tarde!")
    else:
        falar("Boa noite!")
    falar("Como posso ajudar você?")

def main():
    """Função principal para executar o assistente."""
    saudar()

    while True:
        comando = ouvir()
        if not comando:
            continue

        if "horas" in comando:
            dizer_horas()
        elif "data" in comando:
            dizer_data()
        elif "wikipedia" in comando:
            consulta = comando.replace("wikipedia", "").strip()
            pesquisar_wikipedia(consulta)
        elif "tocar música" in comando:
            nome_musica = comando.replace("tocar música", "").strip()
            tocar_musica(nome_musica)
        elif "captura de tela" in comando:
            capturar_tela()
        elif "piada" in comando:
            contar_piada()
        elif "abrir youtube" in comando:
            falar("Abrindo o YouTube.")
            wb.open("https://www.youtube.com")
        elif "abrir google" in comando:
            falar("Abrindo o Google.")
            wb.open("https://www.google.com")

        elif "sair" in comando or "desligar" in comando:
            falar("Até logo! Foi um prazer ajudar você.")
            break

if __name__ == "__main__":
    main()
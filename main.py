from kivy.app import App
from kivy.lang import Builder
import requests
import speech_recognition as sr
import pyttsx3
import datetime
import threading

KV = '''
FloatLayout:

    canvas.before:
        Color:
            rgb: 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos

    Label:
        text: "J.A.R.V.I.S"
        font_size: 48
        pos_hint: {"center_x":0.5, "top":0.95}
        color: 0,1,1,1

    Label:
        id: status
        text: "Aguardando comando..."
        pos_hint: {"center_x":0.5, "top":0.85}
        color: 0,1,0,1

    Button:
        text: "ATIVAR"
        font_size: 22
        size_hint: 0.4,0.2
        pos_hint: {"center_x":0.5, "center_y":0.3}
        on_press: app.ouvir_comando()
'''

class JarvisApp(App):

    def build(self):
        self.engine = pyttsx3.init()
        threading.Thread(target=self.escuta_continua, daemon=True).start()
        return Builder.load_string(KV)

    def falar(self, texto):
        self.root.ids.status.text = texto
        self.engine.say(texto)
        self.engine.runAndWait()

    def escuta_continua(self):
        r = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                texto = r.recognize_google(audio, language="pt-BR").lower()
                if "jarvis" in texto:
                    self.falar("Sim?")
                    self.ouvir_comando()
            except:
                pass

    def ouvir_comando(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.root.ids.status.text = "Ouvindo..."
            audio = r.listen(source)

        try:
            comando = r.recognize_google(audio, language="pt-BR")
            self.processar(comando)
        except:
            self.falar("Não entendi")

    def processar(self, comando):

        # OFFLINE
        if "hora" in comando:
            agora = datetime.datetime.now().strftime("%H:%M")
            self.falar(f"Agora são {agora}")
            return

        if "quem é você" in comando:
            self.falar("Eu sou Jarvis, sua inteligência artificial pessoal")
            return

        # ONLINE
        try:
            resposta = requests.get(
                "https://api.affiliateplus.xyz/api/chatbot",
                params={"message": comando, "botname": "Jarvis"}
            ).json()

            self.falar(resposta["message"])

        except:
            self.falar("Sem internet")

JarvisApp().run()

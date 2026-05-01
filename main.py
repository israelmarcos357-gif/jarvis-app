from kivy.app import App
from kivy.lang import Builder
import requests

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

    TextInput:
        id: entrada
        hint_text: "Digite seu comando..."
        size_hint: 0.8, 0.1
        pos_hint: {"center_x":0.5, "center_y":0.5}

    Label:
        id: resposta
        text: "Sistema pronto"
        pos_hint: {"center_x":0.5, "center_y":0.35}
        color: 0,1,0,1

    Button:
        text: "ENVIAR"
        size_hint: 0.4, 0.1
        pos_hint: {"center_x":0.5, "center_y":0.2}
        on_press: app.perguntar()
'''

class JarvisApp(App):

    def build(self):
        return Builder.load_string(KV)

    def perguntar(self):
        comando = self.root.ids.entrada.text

        if not comando:
            self.root.ids.resposta.text = "Digite algo"
            return

        try:
            r = requests.get(
                "https://api.affiliateplus.xyz/api/chatbot",
                params={"message": comando, "botname": "Jarvis"}
            ).json()

            self.root.ids.resposta.text = r["message"]

        except:
            self.root.ids.resposta.text = "Erro de conexão"

JarvisApp().run()

from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp


class MainApp(MDApp):
    def __init__(self=None, **kwargs):
        self.title = "Abraar's Blog"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        super().__init__(**kwargs)


class MyLayout(BoxLayout):
    def post_text(self):
        text = self.input.text
        self.output.text = text


if __name__ == '__main__':
    app = MainApp()
    app.run()

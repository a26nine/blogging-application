from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
import sqlite3 as sql

from kivymd.uix.label import MDLabel


class MainApp(MDApp):
    def __init__(self=None, **kwargs):
        self.title = "Abraar's Blog"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        super().__init__(**kwargs)
        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS content (post TEXT)""")
        con.commit()
        con.close()


class MyLayout(BoxLayout):
    def post_text(self):
        text = self.input.text
        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("""INSERT INTO content (post) VALUES (?)""", (text,))
        con.commit()
        cur.execute("""SELECT * FROM content""")
        count = cur.fetchall()
        for c in count[0:5]:
            old_text = c[0]
            blog_str = "BLOG #" + str(count.index(c)+1)
            self.output.add_widget(MDLabel(text=blog_str))
            self.output.add_widget(MDLabel(text=old_text))
        con.close()


if __name__ == '__main__':
    app = MainApp()
    app.run()

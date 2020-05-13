import sqlite3 as sql

from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
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
        con.close()

    def load_blog(self):
        self.output.clear_widgets()
        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("""SELECT * FROM content""")
        count = cur.fetchall()
        blog_number = len(count)
        for c in reversed(count):
            old_text = c[0]
            blog_str = "BLOG #" + str(blog_number)
            self.output.add_widget(MDLabel(text=blog_str, size_hint_y=None))
            self.output.add_widget(MDLabel(text=old_text, size_hint_y=None))
            blog_number -= 1
        con.close()


if __name__ == '__main__':
    app = MainApp()
    app.run()

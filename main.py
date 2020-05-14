import sqlite3 as sql

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

blog_db = "blog.db"
create_blog_query = "CREATE TABLE IF NOT EXISTS content (post TEXT)"
read_blog_query = "INSERT INTO content (post) VALUES (?)"


class MainApp(MDApp):
    def __init__(self=None, **kwargs):
        self.title = "FLOW OF THOUGHTS"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        super().__init__(**kwargs)
        con = sql.connect(blog_db)
        cur = con.cursor()
        cur.execute(create_blog_query)
        con.commit()
        con.close()


class HomeScreen(MDScreen):
    def load_blog(self):
        self.all_posts.clear_widgets()
        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("""SELECT * FROM content""")
        count = cur.fetchall()
        blog_number = len(count)
        for c in reversed(count):
            old_text = c[0]
            blog_str = "BLOG #" + str(blog_number)
            self.all_posts.add_widget(MDLabel(text=blog_str, size_hint_y=None))
            self.all_posts.add_widget(MDLabel(text=old_text, size_hint_y=None))
            blog_number -= 1
        con.close()

    def post_text(self):
        text = self.input.text
        con = sql.connect(blog_db)
        cur = con.cursor()
        cur.execute(read_blog_query, (text,))
        con.commit()
        con.close()


class RegistrationScreen(MDScreen):
    pass


class WindowManager(ScreenManager):
    pass


if __name__ == '__main__':
    app = MainApp()
    app.run()

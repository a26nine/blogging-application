import sqlite3 as sql

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

blog_db = "blog.db"
create_blog_query = "CREATE TABLE IF NOT EXISTS content (blogid INTEGER PRIMARY KEY," \
                    "time DATETIME DEFAULT CURRENT_TIMESTAMP, title TEXT, content TEXT," \
                    "file BLOB, isprivate Integer)"
read_blog_query = "INSERT INTO content (title, content, file, isprivate) VALUES (?,?,?,?)"
isprivate = 0
blob_path = ""


def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def write_data(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
        toast("Downloaded!")


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
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            previous=True,
        )

    def on_checkbox_active(self, checkbox, value):
        global isprivate
        if value:
            isprivate = 1
        else:
            isprivate = 0

    def file_manager_open(self):
        self.file_manager.show('/')
        self.manager_open = True

    def select_path(self, path):
        global blob_path
        blob_path = path
        self.exit_manager()
        toast(path)

    def exit_manager(self):
        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True


class HomeScreen(MDScreen):
    def post_text(self):
        title = self.title.text
        content = self.content.text
        if blob_path != "":
            blob = convert_to_binary(blob_path)
        else:
            blob = "NULL"
        con = sql.connect(blog_db)
        cur = con.cursor()
        cur.execute(read_blog_query, (title, content, blob, isprivate,))
        con.commit()
        con.close()


class RegistrationScreen(MDScreen):
    pass


class BlogScreen(MDScreen):
    def on_enter(self, *args):
        # self.clear_widgets()
        con = sql.connect("blog.db")
        cur = con.cursor()
        cur.execute("""SELECT * FROM content""")
        count = cur.fetchall()
        blog_number = len(count)
        for c in reversed(count):
            old_text = c[0]
            blog_str = "BLOG #" + str(blog_number)
            self.ids.list.add_widget(MDLabel(text=blog_str))
            self.ids.list.add_widget(MDLabel(text=old_text))
            blog_number -= 1
        con.close()


class WindowManager(ScreenManager):

    def change_screen(self, screen):
        self.current = screen


if __name__ == '__main__':
    app = MainApp()
    app.run()

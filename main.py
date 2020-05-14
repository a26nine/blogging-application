import sqlite3 as sql
import re
import base64

from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

blog_db = "blog.db"
create_content_query = "CREATE TABLE IF NOT EXISTS content (blogid INTEGER PRIMARY KEY," \
                    "time DATETIME DEFAULT CURRENT_TIMESTAMP, title TEXT, content TEXT," \
                    "file BLOB, isprivate Integer)"
create_users_query = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY," \
                     "password TEXT, isadmin Integer)"
first_user_query = "INSERT OR IGNORE INTO users (username, password, isadmin) VALUES (?,?,?)"
post_blog_query = "INSERT INTO content (title, content, file, isprivate) VALUES (?,?,?,?)"
register_user_query = "INSERT INTO users (username, password, isadmin) VALUES (?,?,?)"
isprivate = 0
blob_path = ""
regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
regex_password = '[A-Z]', '[a-z]', '[0-9]'
admin_email = "admin@fot.com"
admin_password = base64.b16encode("admin@2020".encode("utf-8"))


def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def write_data(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
        toast("Downloaded!")


def check_email(email):
    if re.search(regex_email, email):
        return True


def check_password(password):
    if len(password) >= 8 and all(re.search(r, password) for r in regex_password):
        return True


class MainApp(MDApp):
    def __init__(self=None, **kwargs):
        self.title = "FLOW OF THOUGHTS"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        super().__init__(**kwargs)
        con = sql.connect(blog_db)
        cur = con.cursor()
        cur.execute(create_content_query)
        cur.execute(create_users_query)
        cur.execute(first_user_query, (admin_email, admin_password, 1))
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
        cur.execute(post_blog_query, (title, content, blob, isprivate,))
        con.commit()
        con.close()


class RegistrationScreen(MDScreen):
    def register(self):
        username = self.username.text
        password = self.password.text
        if check_email(username) is True:
            if check_password(password) is True:
                encrypted_password = base64.b64encode(password.encode("utf-8"))
                con = sql.connect(blog_db)
                cur = con.cursor()
                cur.execute(register_user_query, (username, encrypted_password, 0))
                con.commit()
                con.close()
                toast("Registration successful!")
            else:
                toast(
                    "Please enter a strong password! (min 8 character, min 1 lowercase, min 1 uppercase, min 1 digit)",
                    duration=9)
        else:
            toast("Invalid email address!")


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

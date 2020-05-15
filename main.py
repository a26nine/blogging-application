import base64
import re
import sqlite3 as sql

import geocoder
import httpagentparser
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

blog_db = "blog.db"
blob_path = ""
create_content_query = "CREATE TABLE IF NOT EXISTS content (blogid INTEGER PRIMARY KEY," \
                       "time DATETIME DEFAULT CURRENT_TIMESTAMP, title TEXT, content TEXT," \
                       "file BLOB, isprivate Integer)"
create_users_query = "CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY," \
                     "password TEXT, isadmin Integer)"
create_log_query = "CREATE TABLE IF NOT EXISTS log (time DATETIME DEFAULT CURRENT_TIMESTAMP," \
                   "activity TEXT, email TEXT, ip TEXT, location TEXT, device TEXT)"
first_user_query = "INSERT OR IGNORE INTO users (email, password, isadmin) VALUES (?,?,?)"
post_blog_query = "INSERT INTO content (title, content, file, isprivate) VALUES (?,?,?,?)"
register_user_query = "INSERT INTO users (email, password, isadmin) VALUES (?,?,?)"
insert_log_query = "INSERT INTO log (activity, email, ip, location, device) VALUES (?,?,?,?,?)"
admin_email = "admin@fot.com"
admin_password = base64.b64encode("Admin@2020".encode("utf-8"))
regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
regex_password = '[A-Z]', '[a-z]', '[0-9]'
ua = 'Mozilla/5.0 (Linux; Android 4.3; C5502 Build/10.4.1.B.0.101)' \
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.136 Mobile Safari/537.36'
isprivate = 0


def convert_to_binary(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def write_data(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
        toast("Downloaded!")


def check_email_valid(email):
    if re.search(regex_email, email):
        return True


def check_password_strength(password):
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
        cur.execute(create_log_query)
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
        con = sql.connect(blog_db)
        cur = con.cursor()
        email = self.email.text
        password = self.password.text
        if email == "" or password == "":
            toast("Please enter email/password!")
        else:
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_data = cur.fetchone()
            if user_data is None:
                toast("User does not exist!")
            else:
                if base64.b64decode(user_data[1]).decode("utf-8") == password:
                    title = self.title.text
                    content = self.content.text
                    if title == "" or content == "":
                        toast("Please enter title and content!")
                    else:
                        if isprivate == 1:
                            content = base64.b64encode(content.encode("utf-8"))
                        if blob_path != "":
                            blob = convert_to_binary(blob_path)
                        else:
                            blob = "NULL"
                        location_raw = geocoder.ip('me')
                        ip = location_raw.ip
                        location = location_raw.city + ", " + location_raw.state + ", " + location_raw.country
                        device = str(httpagentparser.simple_detect(ua))
                        cur.execute(post_blog_query, (title, content, blob, isprivate))
                        cur.execute(insert_log_query, ("new_post", email, ip, location, device))
                        con.commit()
                        last_blog_id = cur.execute("SELECT rowid from content order by ROWID DESC limit 1").fetchone()
                        toast(("Post successful! Blog #" + str(last_blog_id[0])), 9)
                else:
                    toast("Invalid password!")
        con.close()


class ListScreen(MDScreen):
    def on_enter(self, *args):
        con = sql.connect(blog_db)
        cur = con.cursor()
        cur.execute("""SELECT * FROM content""")
        count = cur.fetchall()
        for c in reversed(count):
            blog_id = c[0]
            title = c[2]
            blog_str = "BLOG #" + str(blog_id)
            self.ids.post_list.add_widget(MDLabel(text=blog_str))
            self.ids.post_list.add_widget(MDLabel(text=title))
        location_raw = geocoder.ip('me')
        ip = location_raw.ip
        location = location_raw.city + ", " + location_raw.state + ", " + location_raw.country
        device = str(httpagentparser.simple_detect(ua))
        cur.execute(insert_log_query, ("list_posts", "guest", ip, location, device))
        con.commit()
        con.close()

    def on_leave(self, *args):
        self.ids.post_list.clear_widgets()


class PostScreen(MDScreen):
    pass


class RegistrationScreen(MDScreen):
    def register(self):
        email = self.email.text
        password = self.password.text
        if check_email_valid(email) is True:
            if check_password_strength(password) is True:
                encrypted_password = base64.b64encode(password.encode("utf-8"))
                con = sql.connect(blog_db)
                cur = con.cursor()
                cur.execute(register_user_query, (email, encrypted_password, 0))
                location_raw = geocoder.ip('me')
                ip = location_raw.ip
                location = location_raw.city + ", " + location_raw.state + ", " + location_raw.country
                device = str(httpagentparser.simple_detect(ua))
                cur.execute(insert_log_query, ("user_registration", email, ip, location, device))
                con.commit()
                con.close()
                toast("Registration successful!")
            else:
                toast(
                    "Please enter a strong password! (min 8 character, min 1 lowercase, min 1 uppercase, min 1 digit)",
                    duration=9)
        else:
            toast("Invalid email address!")


class WindowManager(ScreenManager):

    def change_screen(self, screen):
        self.current = screen


if __name__ == '__main__':
    app = MainApp()
    app.run()

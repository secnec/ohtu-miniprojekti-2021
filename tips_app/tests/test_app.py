import unittest

from tips_app import create_app
from tips_app.routes import register
from tips_app.models import Users, Tips


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app, self.db = create_app(database_uri=f"sqlite://", secret_key="TEST1234")

        with self.app.app_context():
            with open("schema.sql", "r") as file:
                script = file.read().replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY")
                for line in script.split("\n"):
                    self.db.engine.execute(line)

        self.client = self.app.test_client()
        
        self.register("testuser", "pass1234", "pass1234")
        self.register("testuser2", "pass4321", "pass4321")

    def register(self, username, password, password_confirmation):
        data = {
            "username": username,
            "password": password,
            "password_confirmation": password_confirmation,
        }
        return self.client.post(
            "/register",
            data=data,
            follow_redirects=True,
        )

    def signin(self, username, password):
        data = {
            "username": username,
            "password": password
        }
        return self.client.post(
            "/signin",
            data=data,
            follow_redirects=True
        )

    def test_register_and_register_with_unavailable_username_works(self):
        res = self.client.get("/register")
        self.assertIn(b"Registration page", res.data)

        res = self.register("asder", "password1234", "password1234")

        with self.app.app_context():
            user = (
                self.db.session.query(Users.username)
                .filter(Users.username == "asder")
                .first()
            )
        self.assertEqual(user.username, "asder")

        res = self.register("asder", "password", "password")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()

        self.assertEqual(user_count, 3)
    
    def test_register_with_invalid_credentials_works(self):
        res = self.register("usernami", "PAS", "PAS")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 2)

        res = self.register("us", "password1234", "password1234")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 2)

        res = self.register("usernami", "pa$$w0rd1234", "paaassswooord")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 2)

    def test_index_page_opens(self):
        response = self.client.get("/")
        self.assertIn(b"Opening page", response.data)
    
    def input_search_word(self, word):
        data = {"searchtitle": word}
        return self.client.post("/", data=data)

    def test_index_search_too_short(self):
        response = self.input_search_word("a")
        self.assertIn(b"Search text must be at least 3 characters long.", response.data)
    
    def test_index_search_fails(self):
        response = self.input_search_word("thisnotindatabase")
        self.assertIn(b"No tip titles contain: thisnotindatabase", response.data)

    def test_index_search_succeeds(self):
        self.add_tip_as_testuser("helsingin sanomat", "https://www.hs.fi/")
        self.add_tip_as_testuser("ilta-sanomat", "https://www.is.fi/")
        response = self.input_search_word("hel")
        self.assertIn(b"helsingin sanomat", response.data)

    def test_signin_redirects_to_add_tips_page_with_valid_credentials(self):
        signin = self.signin("testuser", "pass1234")
        self.assertIn(b"Add a new reading tip", signin.data)

    def test_signin_results_in_error_message_with_invalid_username(self):
        signin = self.signin("", "875878687")
        self.assertIn(b"Invalid username or password", signin.data)

    def test_signin_results_in_error_message_with_incorrect_username(self):
        signin = self.signin("testuser", "875878687")
        self.assertIn(b"Invalid username or password", signin.data)

    def test_sign_in_link_exists_when_user_is_not_signed_in(self):
        index = self.client.get("/")
        self.assertIn(b"Sign-in", index.data)

    def test_sign_in_link_is_hidden_when_user_is_signed_in(self):
        signin = self.signin("testuser", "pass1234")
        self.assertNotIn(b"Sign-in", signin.data)

    def test_going_to_sign_in_page_while_signed_in_redirects_to_index(self):
        self.signin("testuser", "pass1234")
        attempt = self.client.get("/signin", follow_redirects=True)
        self.assertIn(b"Opening page", attempt.data)

    def add_tip_as_testuser(self, title, url):
        self.signin("testuser", "pass1234")
        data = {
            "username": "testuser",
            "title": title,
            "url": url
        }
        return self.client.post("/add", data=data, follow_redirects=True)

    def add_tip_as_testuser2(self, title, url):
        self.signin("testuser2", "pass4321")
        data = {
            "username": "testuser",
            "title": title,
            "url": url
        }
        return self.client.post("/add", data=data, follow_redirects=True)
    
    def test_nonexistent_tips_wont_appear_on_index(self):
        index = self.client.get("/")
        self.assertNotIn(b"sahara", index.data)
    
    def test_added_tip_appears_on_index(self):
        self.add_tip_as_testuser("sahara", "https://en.wikipedia.org/wiki/Sahara")
        index = self.client.get("/")
        self.assertIn(b"sahara", index.data)

    def test_added_tip_is_a_link(self):
        self.add_tip_as_testuser("sahara", "https://en.wikipedia.org/wiki/Sahara")
        index = self.client.get("/")
        self.assertIn(b"<a href=https://en.wikipedia.org/wiki/Sahara> sahara </a>", index.data)

    def test_tips_db_is_empty_at_first(self):
        with self.app.app_context():
           tip_count = self.db.session.query(Tips.id).count()

        self.assertEqual(tip_count, 0)
        
    def test_valid_tip_is_added(self):
        self.add_tip_as_testuser("himalaja", "https://fi.wikipedia.org/wiki/Himalaja")
                
        with self.app.app_context():
           tip_count = self.db.session.query(Tips.id).count()

        self.assertEqual(tip_count, 1)

        with self.app.app_context():
            tip = (
                self.db.session.query(Tips.title)
                .filter(Tips.title == "himalaja")
                .first()
            )
        self.assertEqual(tip.title, "himalaja")

    def test_tip_without_title_fails(self):
        add = self.add_tip_as_testuser("hi", "https://fi.wikipedia.org/wiki/Himalaja")
        self.assertIn(b"Tip must have an URL and a title at least 3 characters long.", add.data)

    def test_tip_without_url_fails(self):
        add = self.add_tip_as_testuser("himalaja", " ")
        self.assertIn(b"Tip must have an URL and a title at least 3 characters long.", add.data)
    
    def logout(self):
        return self.client.get("/logout", follow_redirects = True)

    def test_logout(self):
        self.signin("testuser", "pass1234")
        logout = self.logout()
        self.assertIn(b"Opening page", logout.data)


    def add_and_remove_tip_as_testuser(self, title, url):
        self.add_tip_as_testuser(title, url)
        with self.app.app_context():
            tip = (
                self.db.session.query(Tips.id)
                .filter(Tips.title == title)
                .first()
            )
        del_data = {
            "username": "testuser", 
            "tip_id_to_delete": tip[0]
            }
        return self.client.post("/delete", data=del_data, follow_redirects=True)

    def test_removed_tip_not_on_index(self):
        self.add_and_remove_tip_as_testuser("sahara", "https://en.wikipedia.org/wiki/Sahara")
        index = self.client.get("/")
        self.assertNotIn(b"sahara", index.data)

    def test_removed_tip_not_on_user_page(self):
        self.add_and_remove_tip_as_testuser("sahara", "https://en.wikipedia.org/wiki/Sahara")
        index = self.client.get("/user")
        self.assertNotIn(b"sahara", index.data)
        
    def test_user_page_shows_tip(self):
        self.add_tip_as_testuser("google", "https://google.com")
        userpage = self.client.get("/user")
        self.assertIn(b"google", userpage.data)

    def test_user_page_shows_tip_only_if_it_was_made_by_signed_in_user(self):
        self.add_tip_as_testuser("helsinki", "https://fi.wikipedia.org/wiki/Helsinki")
        self.logout()
        self.add_tip_as_testuser2("hanko", "https://fi.wikipedia.org/wiki/Hanko")
        userpage = self.client.get("/user")
        self.assertNotIn(b"helsinki", userpage.data)
        self.assertIn(b"hanko", userpage.data)

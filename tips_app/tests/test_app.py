import unittest

from tips_app import create_app
from tips_app.routes import register
from tips_app.models import Users, Tips


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app, self.db = create_app(database_uri=f"sqlite://", secret_key="TEST1234")

        with self.app.app_context():
            with open("schema.sql", "r") as file:
                for line in file.read().split("\n"):
                    self.db.engine.execute(line)

        self.client = self.app.test_client()
        
        self.register("testuser", "pass1234", "pass1234")

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

        self.assertEqual(user_count, 2)
    
    def test_register_with_invalid_credentials_works(self):
        res = self.register("usernami", "PAS", "PAS")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 1)

        res = self.register("us", "password1234", "password1234")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 1)

        res = self.register("usernami", "pa$$w0rd1234", "paaassswooord")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 1)

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
        pass

    def test_signin_redirects_to_add_tips_page_with_valid_credentials(self):
        signin = self.signin("testuser", "pass1234")
        self.assertIn(b"Add a new reading tip", signin.data)

    def test_signin_results_in_error_message_with_invalid_username(self):
        signin = self.signin("", "875878687")
        self.assertIn(b"Invalid username or password", signin.data)

    def test_signin_results_in_error_message_with_incorrect_username(self):
        signin = self.signin("testuser", "875878687")
        self.assertIn(b"Invalid username or password", signin.data)

    def add_tip_as_testuser(self, title, url):
        self.signin("testuser", "pass1234")
        data = {
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
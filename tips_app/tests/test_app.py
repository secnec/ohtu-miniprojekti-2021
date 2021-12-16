import unittest

from tips_app import create_app
import tips_app
from tips_app.routes import register
from tips_app.models import Likes, Users, Tips


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

        self.assertIn(b"name=\"username\" value=\"asder\"", res.data)
        self.assertIn(b"name=\"password\" value=\"password\"", res.data)
        self.assertIn(b"name=\"password_confirmation\" value=\"password\"", res.data)

    def test_register_with_invalid_credentials_works(self):
        res = self.register("usernami", "PAS", "PAS")
        with self.app.app_context():
            user_count = self.db.session.query(Users.username).count()
        self.assertIn(b"Registration page", res.data)
        self.assertEqual(user_count, 2)

        self.assertIn(b"name=\"username\" value=\"usernami\"", res.data)
        self.assertIn(b"name=\"password\" value=\"PAS\"", res.data)
        self.assertIn(b"name=\"password_confirmation\" value=\"PAS\"", res.data)

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
        self.assertIn(b"name=\"searchtitle\" value=\"a\"", response.data)
    
    def test_index_search_fails(self):
        response = self.input_search_word("thisnotindatabase")
        self.assertIn(b"No tip titles contain: thisnotindatabase", response.data)
        self.assertIn(b"name=\"searchtitle\" value=\"thisnotindatabase\"", response.data)

    def test_index_search_succeeds(self):
        self.add_tip_as_testuser("helsingin sanomat", "https://www.hs.fi/")
        self.add_tip_as_testuser("ilta-sanomat", "https://www.is.fi/")
        response = self.input_search_word("hel")
        self.assertIn(b"helsingin sanomat", response.data)

    def test_signin_redirects_to_user_page_with_valid_credentials(self):
        signin = self.signin("testuser", "pass1234")
        self.assertIn(b"Your own tips", signin.data)

    def test_signin_results_in_error_message_with_invalid_username(self):
        signin = self.signin("", "875878687")
        self.assertIn(b"Invalid username or password", signin.data)
        self.assertIn(b"name=\"username\" value=\"\"", signin.data)
        self.assertIn(b"name=\"password\" value=\"875878687\"", signin.data)

    def test_signin_results_in_error_message_with_incorrect_username(self):
        signin = self.signin("testuser", "875878687")
        self.assertIn(b"Invalid username or password", signin.data)
        self.assertIn(b"name=\"username\" value=\"testuser\"", signin.data)
        self.assertIn(b"name=\"password\" value=\"875878687\"", signin.data)

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

    def test_succesfull_add_tip_redirects_to_user_page(self):
        add = self.add_tip_as_testuser("himalaja", "https://fi.wikipedia.org/wiki/Himalaja")
        self.assertIn(b"Your own tips", add.data)

    def test_tip_without_title_fails(self):
        add = self.add_tip_as_testuser("hi", "https://fi.wikipedia.org/wiki/Himalaja")
        self.assertIn(b"Tip must have an URL and a title at least 3 characters long.", add.data)
        self.assertIn(b"name=\"title\" value=\"hi\"", add.data)
        self.assertIn(b"name=\"url\" value=\"https://fi.wikipedia.org/wiki/Himalaja\"", add.data)

    def test_tip_without_url_fails(self):
        add = self.add_tip_as_testuser("himalaja", " ")
        self.assertIn(b"Tip must have an URL and a title at least 3 characters long.", add.data)
        self.assertIn(b"name=\"title\" value=\"himalaja\"", add.data)
        self.assertIn(b"name=\"url\" value=\" \"", add.data)

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

    def like_tip(self, username, tip_id):
        data = {
            "username": username,
            "tip_id": tip_id
        }
        return self.client.post(
            "/like",
            data=data,
            follow_redirects=True
        )

    def test_liking_raises_like_counter(self):
        self.add_tip_as_testuser("oulu", "https://fi.wikipedia.org/wiki/Oulu")
        self.like_tip("testuser", 1)
        self.logout()
        self.signin("testuser2", "pass4321")
        self.like_tip("testuser2", 1)
        with self.app.app_context():
            like_amount = (
                    self.db.session.query(Tips.likes)
                    .filter(Tips.title == "oulu")
                    .first()[0]
                )
        self.assertEqual(like_amount, 2)

    def test_unliking_removes_like_when_logged_in(self):
        self.add_tip_as_testuser("Tippy Tip", "https://google.com")
        self.like_tip("testuser", 1)

        with self.app.app_context():
            like_count = self.db.session.query(Likes).count()
            tippy_count = self.db.session.query(Tips).first().likes
        self.assertEqual(like_count, 1)
        self.assertEqual(tippy_count, 1)

        self.like_tip("testuser", 1)

        with self.app.app_context():
            like_count = self.db.session.query(Likes).count()
            tippy_count = self.db.session.query(Tips).first().likes
        self.assertEqual(like_count, 0)
        self.assertEqual(tippy_count, 0)

        self.like_tip("testuser", 1)
        self.logout()
        self.like_tip("testuser", 1)

        with self.app.app_context():
            like_count = self.db.session.query(Likes).count()
            tippy_count = self.db.session.query(Tips).first().likes
        self.assertEqual(like_count, 1)
        self.assertEqual(tippy_count, 1)


    def test_unliking_removes_correct_like(self):
        self.add_tip_as_testuser("Tippy Tip", "https://google.com")
        self.like_tip("testuser", 1)

        self.logout()

        index_contents = self.client.get("/").data
        self.assertNotIn(b"Like", index_contents)

        self.add_tip_as_testuser2("Top of the Tip", "https://google.com")

        self.like_tip("testuser2", 2)

        index_contents = self.client.get("/").data
        self.assertIn(b"Unlike", index_contents)
        self.assertIn(b"Like", index_contents)

        with self.app.app_context():
            like_count = self.db.session.query(Likes).count()
            tippy_count = self.db.session.query(Tips).filter(Tips.id == 1).first().likes
            top_count = self.db.session.query(Tips).filter(Tips.id == 2).first().likes
        self.assertEqual(like_count, 2)
        self.assertEqual(tippy_count, 1)
        self.assertEqual(top_count, 1)

        self.like_tip("testuser2", 2)

        with self.app.app_context():
            like_count = self.db.session.query(Likes).count()
            tippy_like = self.db.session.query(Likes).filter(Likes.tip_id == 1).first()
            tippy_count = self.db.session.query(Tips).filter(Tips.id == 1).first().likes
            top_count = self.db.session.query(Tips).filter(Tips.id == 2).first().likes
        self.assertEqual(like_count, 1)
        self.assertIsNotNone(tippy_like)
        self.assertEqual(tippy_count, 1)
        self.assertEqual(top_count, 0)


    def test_likes_show_up_right(self):
        self.add_tip_as_testuser("tip1", "https://www.wikipedia.org")
        self.like_tip("testuser", 1)
        self.add_tip_as_testuser("tip2", "https://www.wikipedia.org")
        self.like_tip("testuser", 2)
        self.logout()

        self.signin("testuser2", "pass4321")
        self.like_tip("testuser2", 2)
        self.logout()
        
        index = self.client.get("/").data

        self.assertIn(b"2 likes", index)
        self.assertIn(b"1 likes", index)
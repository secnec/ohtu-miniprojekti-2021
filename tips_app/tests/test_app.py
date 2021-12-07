import unittest
import os
import tempfile

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

    def test_register_works(self):
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
            users = (
                self.db.session.query(Users.username)
                .filter(Users.username == "asder")
                .all()
            )

        self.assertIn(b"Registration page", res.data)
        self.assertEqual(len(users), 1)

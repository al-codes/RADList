import unittest

from server import app
from model import db, connect_to_db
import seed
import crud

class LoginTests(unittest.TestCase):
    """Tests for login page"""

    def setUp(self):
        """Steps to take before every test"""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///radlist")
        db.create_all()
        crud.create_fake_data()

    def tearDown(self):
        """Steps to take after every test"""

        db.session.close()
        db.drop_all()

    def test_no_existing_user(self):
        """Test login where no account exists for given username"""

        result = self.client.post("/login",
                                  data={"email": "frank@test.com", 
                                        "password": "frankie"},
                                  follow_redirects=True)

        self.assertIn(b"This account does not exist.", result.data)
        self.assertNotIn(b"Users", result.data)

    def test_wrong_password(self):
        """Test login where wrong password given for existing username"""

        result = self.client.post("/login",
                                  data={"email": "anne@test.com", 
                                        "password": "blah"},
                                  follow_redirects=True)

        self.assertIn(b"Incorrect email or password.", result.data)
        self.assertNotIn(b"Users", result.data)

    def test_correct_login(self):
        """Test login where username and password are correct"""

        result = self.client.post("/login",
                                  data={"email": "anne@test.com", 
                                        "password": "anne"},
                                  follow_redirects=True)

        self.assertIn(b"Give us your favorite artist", result.data)
        self.assertNotIn(b'placeholder="password"', result.data)




if __name__ == "__main__":
    unittest.main()
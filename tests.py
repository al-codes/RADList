from unittest import TestCase
from server import app
from model import connect_to_db, db, create_fake_data
import crud
import helper





class FlaskTests(TestCase):
    """ Flask tests """

    def setUp(self):
        """ Set up test """

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        """ Test homepage """

        result = self.client.get("/")
        self.assertIn(b"New to RAD List", result.data)

class LoginTests(TestCase):
    """Tests for login page"""

    def setUp(self):
        """ Set up test """

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        create_fake_data()

    def tearDown(self):
        """ Tear down test """

        db.session.close()
        db.drop_all()

    def test_no_existing_user(self):
        """ Test login where no account exists for given email """

        result = self.client.post("/login",
                                  data={"email": "frank@test.com", 
                                        "password": "frankie"},
                                  follow_redirects=True)

        self.assertIn(b"This account does not exist.", result.data)
        self.assertNotIn(b"Users", result.data)

    def test_wrong_password(self):
        """ Test login where wrong password given for existing email """

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

class CrudTests(TestCase):
    """ Tests for crud """

    def setUp(self):
        """ Set up test """

        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        create_fake_data()


    def tearDown(self):
        """ Tear down test """

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


    def test_create_user(self):
        """ Tests create user function """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        self.assertIsNotNone(user.user_id)


    def test_create_track(self):
        """ Tests create track function """

        track = crud.create_track('You Make me Feel (Mighty Real)', 'Sylvester', '00:06:36')
        self.assertIsNotNone(track.track_id)


    def test_create_playlist(self):
        """ Tests create playlist function """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        playlist = crud.create_playlist(user, 'Test Playlist')
        self.assertIsNotNone(playlist.playlist_id)
    

    def test_create_playlist_track(self):
        """ Tests create playlist track function """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        playlist = crud.create_playlist(user, 'Test Playlist')
        track = crud.create_track('You Make me Feel (Mighty Real)', 'Sylvester', '00:06:36')
        playlist_track = crud.create_playlist_track(playlist.playlist_id, track.track_id)
        self.assertIsNotNone(playlist_track.playlist_track_id)


    def test_get_user_by_email(self):
        """ Tests retrieving user by email function """

        user = crud.get_user_by_email('anne@test.com')
        self.assertIsNotNone(user.user_id)


    def test_get_user_playlist(self):
        """ Tests retrieving a user playlist function """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        playlist = crud.create_playlist(user, 'Test Playlist')
        self.assertIsNotNone(playlist.user_id)


    def test_get_playlist_by_id(self):
        """ Test retrieving a playlist by playlist id """
        
        self.assertIsNotNone(crud.get_user_by_email('anne@test.com'), 1)


    # def test_get_track(self):
    #     """ Gets a track by track ID """

    #     return Track.query.get(track_id)


    # def test_get_track_id(self):
    #     """ Gets track ID by title of song """
    
    #     track_obj = Track.query.filter(Track.title == title).first()

    #     if track_obj:
    #         return str(track_obj.track_id)


    # def test_get_title_by_track_id(self):
    #     """ Gets track name by track ID """

    #     track_obj = Track.query.filter(Track.track_id == track_id).first()

    #     if track_obj:
    #         return str(track_obj.title)



if __name__ == "__main__":
    from server import app
    connect_to_db(app)
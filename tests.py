""" Tests for RAD List """

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
        """ Tests create user """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        self.assertIsNotNone(user.user_id)


    def test_create_track(self):
        """ Tests create track """

        track = crud.create_track('You Make me Feel (Mighty Real)', 'Sylvester', '00:06:36')
        self.assertIsNotNone(track.track_id)


    def test_create_playlist(self):
        """ Tests create playlist """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        playlist = crud.create_playlist(user, 'Test Playlist')
        self.assertIsNotNone(playlist.playlist_id)
    

    def test_create_playlist_track(self):
        """ Tests create playlist track """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        playlist = crud.create_playlist(user, 'Test Playlist')
        track = crud.create_track('You Make me Feel (Mighty Real)', 'Sylvester', '00:06:36')
        playlist_track = crud.create_playlist_track(playlist.playlist_id, track.track_id)
        self.assertIsNotNone(playlist_track.playlist_track_id)


    def test_get_user_by_email(self):
        """ Tests retrieving user by email """

        user = crud.get_user_by_email('anne@test.com')
        self.assertIsNotNone(user.user_id)


    def test_get_user_playlist(self):
        """ Tests retrieving a user playlist """

        user = crud.create_user('andrea@testcom', 'test', 'Andrea', 'Del Rio')
        playlist = crud.create_playlist(user, 'Test Playlist')
        self.assertIsNotNone(crud.get_user_playlist(str(user.user_id)))


    def test_get_playlist_by_id(self):
        """ Tests retrieving a playlist by playlist id """
        
        self.assertEqual((str(crud.get_playlist_by_id('1').playlist_id)), '1')


    def test_get_track(self):
        """ Tests retrieving a track by track ID """

        self.assertEqual((str(crud.get_track('1').track_id)), '1')


    def test_get_track_id(self):
        """ Tests retrieving track ID by title of song """

        self.assertEqual(crud.get_track_id('Common People'), '1')


    def test_get_title_by_track_id(self):
        """ Tests retrieving track name by track ID """

        self.assertEqual(crud.get_title_by_track_id('1'), 'Common People')


    def test_get_artist_by_track_id(self):
        """ Tests retrieving artist name by track ID """

        self.assertEqual(crud.get_artist_by_track_id('1'), 'Pulp')


    def test_get_track_dur(self):
        """ Tests retrieving track duration by track ID """

        self.assertEqual(crud.get_track_dur('1'), '00:03:58')
    
    def test_get_playlist_tracks(playlist_id):
    """ Gets list of all tracks in a user playlist """

        self.assertEqual(crud.get_playlist_tracks('1'), '00:03:58')
    return Playlist_Track.query.filter(Playlist_Track.playlist_id == playlist_id).all()


    def get_playlist_name(playlist_id):
        """ Gets playlist name by ID """

        playlist_obj = Playlist.query.filter(Playlist.playlist_id == playlist_id).first()

        if playlist_obj:
            return playlist_obj.name
    

def get_saved_playlists(user):
    """ Gets all saved user playlists """

    user_playlist_objs = Playlist.query.filter(Playlist.user_id == user).all()
    playlist_names = []

    if user_playlist_objs:
        for up_object in user_playlist_objs:
            playlist_names.append(up_object.name)
    return playlist_names


def get_user_playlist_ids(user):
    """ Gets playlists IDs under user """
    
    user_playlist_objs = Playlist.query.filter(Playlist.user_id == user).all()
    playlist_ids = []
    
    for up_object in user_playlist_objs:
        playlist_ids.append(up_object.playlist_id)
    return playlist_ids


def get_many_artists_by_track_obj(to_lst):
    """ Get a list of artists from a list of track objects """

    artists = []
    for track in to_lst:
        artist = get_artist_by_track_id(track.track_id)
        artists.append(artist)
    return artists


def get_many_tracks_by_track_obj(to_lst):
    """ Get a list of tracks from a list of track objects """
    
    tracks = []
    for track in to_lst:
        track = get_title_by_track_id(track.track_id)
        tracks.append(track)
    return tracks


def get_many_durs_by_track_obj(to_lst):
    """ Get a list of track duratiions from a list of track objects """
    track_durs = []
    for track in to_lst:
        dur = get_track_dur(track.track_id)
        track_durs.append(dur)
    return track_durs




if __name__ == "__main__":
    from server import app
    connect_to_db(app)
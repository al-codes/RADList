""" Seeding the db """

import os, json, crud, server, model


os.system('dropdb radlist')
os.system('createdb radlist')

model.connect_to_db(server.app)
model.db.create_all()

# # Create users
# create_user(fname, lname, email, password)
alex = crud.create_user('alex', 'sanchez', 'asanch@test.com', 'asanch')
pollo = crud.create_user('pollo', 'cat', 'pollo@cat.com', 'luvsnax')
bellina = crud.create_user('bellina', 'kitty', 'bellina@cat.com', 'luvsun')
   
# # Create playlists
# create_playlist(user, name)
crud.create_playlist(alex, 'yacht rockers')
crud.create_playlist(pollo, 'divas')
crud.create_playlist(bellina, 'metal magic')

# # Create tracks
# create_track(title, artist)
crud.create_track('sailin', 'christopher cross')
crud.create_track('paradise', 'sade')
crud.create_track('one', 'metallica')

# #Associate tracks with playlists
# create_playlist_track(playlist_id, track_id)
# crud.create_playlist_track(1, 1)
# crud.create_playlist_track(2, 2)
# crud.create_playlist_track(3, 3)
 



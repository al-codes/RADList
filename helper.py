""" Helper functions """


def create_artist_track_dur_list(artist_list, track_list, dur_list):
    """ Creates a list of artists, tracks and track duration """
    master = []

    for i in range(len(artist_list)):
        master.append([artist_list[i], track_list[i], dur_list[i]])
    return master   


def convert_millis(track_dur_lst):
    """ Convert milliseconds to 00:00:00 format """
    
    converted_track_times = []
    for track_dur in track_dur_lst:
        seconds = (int(track_dur)/1000)%60
        minutes = int(int(track_dur)/60000)
        hours = int(int(track_dur)/(60000*60))
        converted_time = '%02d:%02d:%02d' % (hours, minutes, seconds)
        converted_track_times.append(converted_time)    
    return converted_track_times
   

def create_dict_sim_artists_top_tracks(sa_list, t_tracks):
    """ Creates a dictionary of similar artists and 2 top tracks """

    sim_artists_and_top_tracks = {}

    for i in range(len(sa_list)):
        if sa_list[i] in sim_artists_and_top_tracks:
            sim_artists_and_top_tracks[sa_list[i]].append(t_tracks[i])
        else:
            sim_artists_and_top_tracks[sa_list[i]] = [t_tracks[i]]
    return sim_artists_and_top_tracks   


def create_dict_sim_artists_top_tracks_duration(sa_list, t_tracks, dur_list):
    """ Create a dictionary of similar artists, top tracks and track duration """

    master = {}

    for i in range(len(sa_list)):
        if sa_list[i] in master:
            master[sa_list[i]].extend([t_tracks[i], dur_list[i]])
        else:
            master[sa_list[i]] = [t_tracks[i], dur_list[i]]
    return master


def create_dict_playlists_playlistids(p_list, pid_list):
    """ Create a dictionary of playlists and playlist ids """

    playlists_and_playlist_ids = {}

    for i in range(len(p_list)):
        playlists_and_playlist_ids[p_list[i]] = pid_list[i]
    return playlists_and_playlist_ids

    
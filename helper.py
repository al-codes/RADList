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
   


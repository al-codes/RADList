"use strict"

$.get('/users/profile/api', (data) => {
    $('#user-name').text(`${data.fname} ${data.lname}`);
    $('#user-email').text(data.email);
});


const savedPlaylistsLink = $('#saved-playlists-link');
const savedPlaylist = $('#playlist-links');

$('#list').hide();

savedPlaylistsLink.on('click', (evt) => {
    evt.preventDefault();
    
    savedPlaylistsLink.hide();
    $('#list').show();


});



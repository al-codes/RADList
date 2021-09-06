"use strict"

$.get('/users/profile/api', (data) => {
    $('#user-name').text(`${data.fname} ${data.lname}`);
    $('#user-email').text(data.email);
});
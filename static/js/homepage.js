"use strict"

// process a new user
$('#new-user-submit').on('click', () => {

    const formData = {
        fname: $('#new-fname').val(),
        lname: $('#new-lname').val(),
        email: $('#new-email').val(),
        password: $('#new-password').val(),
        };

    $.post('/users/create-user.json', formData, (response) => {
        $('#new-user-modal').modal('toggle');
        alert(response)
        });
});
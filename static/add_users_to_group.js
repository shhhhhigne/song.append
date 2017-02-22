"use strict";

console.log('hello');


function usersAddedAlert(result) {
    alert('Group users updated');
}


function updateGroupUsers(evt) {

    evt.preventDefault();

    var checkboxes = $(':checkbox');

    var users = {}

    for (var i=0; i<checkboxes.length; i++) {
        users[checkboxes[i]['value']] = {'user_id': checkboxes[i]['value'],
                                         'member': checkboxes[i].checked };
    }

    var formInputs = {'users': users    //                   'group_id': $('#group_id')
    };

    // console.log(typeof($('#group-id').val()))
    var url = '/add-to-group/' + $('#group-id').val();

    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: url,
        data: JSON.stringify(formInputs),
        success: usersAddedAlert,
        dataType: "json"
    });

}


$('#add-users-form').on('submit', updateGroupUsers);
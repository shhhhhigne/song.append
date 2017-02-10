







console.log('hello');


function usersAddedAlert(result) {
    alert('Group users updated');
}


function updateGroupUsers(evt) {

    evt.preventDefault();

    var checkboxes = $(':checkbox')

    // var users = {}

    // for (i=0; i<checkboxes.length; i++) {
    //     users[checkboxes[i]['value']] = {'user_id': checkboxes[i]['value'],
    //                                      'member': checkboxes[i].checked };
    // }

    console.log(users)
    // i probably need to jsonify

    // var formInputs = {'users': users,
    //                   // 'group_id': $('#group_id')
    // };

    var formInputs = {'users': 'meme'};

    var url = '/add-to-group/' + $('#group_id')
    $.post(url,
           formInputs,
           usersAddedAlert
           );
}


$('#add-users-form').on('sumbit', updateGroupUsers);
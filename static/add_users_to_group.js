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

    console.log('heehehehehehehheheheheh')
    console.log(users)

    var formInputs = {'users': users    //                   'group_id': $('#group_id')
    };

    // var formInputs = {"users": {"user1": "hey"}}
    // console.log(formInputs)
    // console.log(JSON.stringify(formInputs))
    // console.log(typeof(JSON.stringify(formInputs)))



    // var formInputs = {'users': 'meme'};

    // var group_id = 

    // console.log(typeof($('#group-id').val()))
    var url = '/add-to-group/' + $('#group-id').val();


    // $.post(url,
    //        JSON.stringify(formInputs),
    //        usersAddedAlert
    //        );

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
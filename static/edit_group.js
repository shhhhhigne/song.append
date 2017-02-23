// function userVoted(results) {

//     console.log(results)

//     var vote_value = results['vote_value'];
//     var ps_id = results['ps_id'];

//     var thumb_id = ps_id + '_' + vote_value + '_thumb';

//     var alt_vote_value = -(vote_value);
//     var alt_thumb_id = ps_id + '_' + alt_vote_value + '_thumb';

//     var vote_status = results['vote_status'];
//     alert(results['user_alert']);

//     var vote_total_id = ps_id + '_total';

//     if (vote_status == 'same') {
//         return;
//     }
//     else if (vote_status == 'changed') {
//         $('#'+alt_thumb_id).removeClass('voted-on');

//     }
//     $('#'+thumb_id).addClass('voted-on');
//     console.log(results['vote_total'])
//     $('#'+vote_total_id).text(results['vote_total']);

//     if (results['status_changed'] == true) {
//         location.reload(true);
//     }

// }

function memberRemoved(results) {
    alert(results)
    location.reload(true);

}

function removeMember() {

    var group_id = $(this).data('group_id');
    var user_id = $(this).data('user_id');

    if ($(this).hasClass('me')) {
        var questionStr = 'Are you sure you want to remove yourself?\n';
        questionStr = questionStr + 'Once you do only others can add ';
        questionStr = questionStr + 'you back and you will no longer have access to playlists shared to this group.';
    }

    else {
        questionStr = 'Are you sure you want to remove this user?';
    }

    var admin_response = confirm(questionStr);

    if (admin_response == false) {
        return
    }

    var removeUserPlaylists = userPlaylists[user_id]

    if (removeUserPlaylists) {
        s = 'If you remove this user from the group, other members will lose access to playlists:\n'
        s = s + ' -> ' + removeUserPlaylists[0]
        for (var i=1; i<removeUserPlaylists.length; i++) {
            s = s + '\n -> ' + removeUserPlaylists[i]
        }
        admin_response = confirm(s)

        if (admin_response == false) {
            return
        }
    }

    var removal_info = {'group_id': group_id,
                        'user_id': user_id
    };


    // $.post('/remove-member/<group_id>/<user_id>',

    $.post('/remove-member',
           removal_info,
           memberRemoved
    );

}

$('.remove_member').on('click', removeMember);


function membersAdded(results) {
    alert(results)
    location.reload(true);

}


function addMember() {
    var group_id = $(this).data('group_id');

    var user_ids = [];
    $('.selectpicker option:selected').each(function() {
        user_ids.push($(this).val());
    });

    var add_info = {'group_id': group_id,
                    'user_ids': user_ids
    };

    $.post('/add-member',
           add_info,
           membersAdded
    );

}

$('.add_member').on('click', addMember);


function newMemberAdmin(results) {
    alert(results)
    location.reload(true);

}

function adminMember() {

    var group_id = $(this).data('group_id');
    var user_id = $(this).data('user_id');

    var admin_response = confirm('Are you sure you want make this user admin?\nIn doing so you will no longer have admin privileges.');

    if (admin_response == false) {
        return
    }

    var new_admin_info = {'group_id': group_id,
                          'user_id': user_id
    };


    // $.post('/remove-member/<group_id>/<user_id>',

    $.post('/admin-member',
           new_admin_info,
           newMemberAdmin
    );

}

$('.admin_member').on('click', adminMember);




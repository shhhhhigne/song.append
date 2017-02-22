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

function removeMember() {

    var group_id = $(this).data('group_id');
    var user_id = $(this).data('user_id');

    var admin_response = confirm('Are you sure you want to remove this user?');

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
        alert(s)

    }

    var removal_info = {'group_id': group_id,
                     'user_id': user_id
    };


    // $.post('/remove-member/<group_id>/<user_id>',
    //        removal_info,
    //        userRemoved
    // );

}

$('.remove_member').on('click', removeMember);

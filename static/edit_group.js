function memberRemoved(results) {
    // alert(results)
    $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: results,
            content: 'This person and this group are no longer connected. All playlist connections are terminated',
            onClose: function() {
                location.reload(true);
            }
        });
    // location.reload(true);

}

function removeMember() {

    var group_id = $(this).data('group_id');
    var user_id = $(this).data('user_id');

    if ($(this).hasClass('me')) {
        var questionTitle = 'Are you sure you want to remove yourself?';
        var questionStr =  'Once you do only others can add you back and you will';
        questionStr = questionStr + ' no longer have access to playlists shared to this group.';
    }

    else {
        questionTitle = 'Are you sure you want to remove this user?';
        questionStr = 'If you do linked playlists will be disconnected';
    }

    var admin_response = $.confirm({
        title: questionTitle,
        content: questionStr,
        onClose: function() {
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
    });

    

}

$('.remove_member').on('click', removeMember);


function membersAdded(results) {
    $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: 'User(s) added',
            content: results + 'and this group are now connected. All playlist connections are in place',
            onClose: function() {
                location.reload(true);
            }
        });

    

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
    // alert(results)
    $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: results,
            content: 'This member is now the admin, you no longer have admin privileges',
            onClose: function() {
                location.reload(true);
            }
        });
    // location.reload(true);

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





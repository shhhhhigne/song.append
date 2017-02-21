// function addSongToPlaylist(song_id, playlist_id) {


//     songIds = {'song_id': song_id,
//                'playlist_id': playlist_id
//     };

//     $.post('/add-song-to-playlist/' + song_id + '/' + playlist_id,
//            songIds,
//            songAddedToPlaylistSuccess
//     );
// }

function userVoted(results) {

    console.log(results)

    var vote_value = results['vote_value'];
    var ps_id = results['ps_id'];

    var thumb_id = ps_id + '_' + vote_value + '_thumb';

    var alt_vote_value = -(vote_value);
    var alt_thumb_id = ps_id + '_' + alt_vote_value + '_thumb';

    var vote_status = results['vote_status'];
    alert(results['alert']);

    var vote_total_id = ps_id + '_total';

    if (vote_status == 'same') {
        return;
    }
    else if (vote_status == 'changed') {
        $('#'+alt_thumb_id).removeClass('voted-on');

    }
    $('#'+thumb_id).addClass('voted-on');
    console.log(results['vote_total'])
    $('#'+vote_total_id).text(results['vote_total']);

    if (results['status_changed'] == true) {
        location.reload(true);
    }

}

function userVote() {

    var thumb_id = $(this).attr('id')

    var vote_info_list = thumb_id.split('_');
    
    var vote_info = {'ps_id': vote_info_list[0],
                     'vote_value': vote_info_list[1],
                     'thumb_id': thumb_id
    };

    $.post('/register-user-vote',
           vote_info,
           userVoted
    );

}

$('.user-vote').on('click', userVote);




function showUserVotes(results) {


    for (var i=0; i<results.length; i++) {

        var vote_value = results[i]['vote_value']
        var ps_id = results[i]['ps_id']

        var thumb_id = ps_id + '_' + vote_value + '_thumb'
        console.log(thumb_id)


        $('#'+thumb_id).addClass('voted-on')

    }

}


checkUserVotes() 

function checkUserVotes() {


    var ps_ids = []
    $.each($('.user-vote-col'), function() {

        ps_id = $(this).attr('id');

        ps_ids.push(ps_id);

        
    });

    ps_data = {'ps_ids': ps_ids};

    $.post('/get-current-user-vote',
            ps_data,
            showUserVotes
    );
}




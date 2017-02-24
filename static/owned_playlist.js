function userVoted(results) {

    console.log(results)

    var vote_value = results['vote_value'];
    var ps_id = results['ps_id'];

    var thumb_id = ps_id + '_' + vote_value + '_thumb';

    var alt_vote_value = -(vote_value);
    var alt_thumb_id = ps_id + '_' + alt_vote_value + '_thumb';

    var vote_status = results['vote_status'];
    alert(results['user_alert']);

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

function removeSong() {

    var ps_id = $(this).data('ps_id')
    
    var remove_info = {'ps_id': ps_id,
    };

    $.post('/remove-song',
           remove_info,
           songRemoved
    );

}

$('.remove-song').on('click', removeSong);
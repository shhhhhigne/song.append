function userVoted(results) {

    console.log(results)

    var vote_value = results['vote_value'];
    var ps_id = results['ps_id'];

    var thumb_id = ps_id + '_' + vote_value + '_thumb';

    var alt_vote_value = -(vote_value);
    var alt_thumb_id = ps_id + '_' + alt_vote_value + '_thumb';

    var vote_status = results['vote_status'];

    if (results['vote_value'] == -1) {
        var alertThumb = "<span class='glyphicon glyphicon-thumbs-down'></span>"

    }
    if (results['vote_value'] == 1) {
        alertThumb = "<span class='glyphicon glyphicon-thumbs-up'></span>"
    }

    var vote_total_id = ps_id + '_total';

    if (vote_status == 'same') { 
        $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: 'You already gave this song a vote of ' + alertThumb,
            content: 'No stuffing the ballot boxes'
        });
        return;
    }
    else if (vote_status == 'changed') {
        $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: 'Your vote is now changed to ' + alertThumb,
            content: "It's ok to change your mind",
            onClose: function() {
                location.reload(true);

            }
        });
        $('#'+alt_thumb_id).removeClass('voted-on');

    }
    else if (vote_status == 'new') {
        $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: 'Your gave a vote of ' + alertThumb,
            content: 'Thank you, your opinion is noted',
            onClose: function() {
                location.reload(true);
            }
        });
    }
    $('#'+thumb_id).addClass('voted-on');
    console.log(results['vote_total'])
    $('#'+vote_total_id).text(results['vote_total']);
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









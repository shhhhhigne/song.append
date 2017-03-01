function songRemoved(results) {
    // alert(results)

    song_name = results['song_name'];
    playlist_name = results['playlist_name'];
    lock_status = results['lock_status'];

    $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: `${song_name} removed from ${playlist_name}`,
            content: `It is ${lock_status}`
        });

    location.reload(true);

}

function removeSong() {

    var ps_id = $(this).data('ps_id');
    
    var remove_info = {'ps_id': ps_id,
    };

    $.post('/remove-song',
           remove_info,
           songRemoved
    );

}

$('.remove-song').on('click', removeSong);



function showLockStatus(results) {


    for (var i=0; i<results.length; i++) {

        var lock_status = results[i]['lock_status'];
        var ps_id = results[i]['ps_id'];

        var lock_id = ps_id + '-lock';
        console.log(lock_id);

        if (lock_status == true) {
            $('#'+lock_id).html('Unlock Song');
            // var lock_li = $('#'+lock_id).parent();
            console.log(lock_li)
            // $(newItemLink).data('song_id', song_id)
            var lock_status_word = 'locked'               
        }
        else if (lock_status == false) {
            $('#'+lock_id).html('Lock in Playlist');
            // console.log($('#'+lock_id).parent())
            console.log(lock_li)
            lock_status_word = 'unlocked'

        }
        var lock_li = $('#'+lock_id).parent();
        $(lock_li).attr('lock_status', lock_status_word)


    }

}

checkLockStatus()

function checkLockStatus() {
    var ps_ids = []
    $.each($('.lock-song'), function() {

        ps_id = $(this).data('ps_id');

        ps_ids.push(ps_id);

        
    });

    ps_data = {'ps_ids': ps_ids};

    $.post('/get-lock-status',
            ps_data,
            showLockStatus
    );
}

function songLockChanged(results) {
    song_name = results['song_name'];
    playlist_name = results['playlist_name'];
    lock_status = results['new_lock_status'];

    if (lock_status == 'locked') {
        var alert_message = 'This means votes will NOT be able to affect its placement on this playlist'
    }
    else if (lock_status == 'unlocked') {
        alert_message = 'This means votes WILL be able to affect its placement on this playlist'
    }

    $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: `${song_name} ${lock_status} in ${playlist_name}`,
            content: alert_message,
            onClose: function () { location.reload(true); }
        });

    // location.reload(true);

}


function lockSong() {

    var ps_id = $(this).data('ps_id');
    var lock_status = $(this).attr('lock_status');
    
    
    var lock_info = {'ps_id': ps_id,
                     'old_lock_status': lock_status
    };

    $.post('/lock-song',
           lock_info,
           songLockChanged
    );
}


$('.lock-song').on('click', lockSong);

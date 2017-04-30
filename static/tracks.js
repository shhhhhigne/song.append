


var audioPlayer = null;
var playing_id = null;
var playing = false; 

var x

// TODO: make click and hold play pop up menu and single click play preview
function setAudioState() {
    x = event
    var evt = event;

    console.log('hello')
    if (audioPlayer == null) {
        audioPlayer = new Audio();
    }

    var target = evt.currentTarget
    var newSong = true;

    if (playing_id != null) {
        if (playing_id != target.id) {
            $('#'+playing_id).removeClass('glyphicon-pause');
            $('#'+playing_id).addClass('glyphicon-play-circle');
        }
        else {
            newSong = false;
            if (audioPlayer.paused) {
                audioPlayer.play();
            }
            else {
                audioPlayer.pause()
            }
        }
    }

    playing_id = target.id

    var play_id = playing_id.split("-")[0]
    
    if (newSong == true) {
        var preview_url = $('#'+playing_id).data('tooltip');
        audioPlayer.src = preview_url;
        audioPlayer.play();
    }

    if (audioPlayer.paused) {
        $('#'+play_id).addClass('glyphicon-play-circle');
        $('#'+play_id).removeClass('glyphicon-pause');
    }
    else {
        $('#'+play_id).removeClass('glyphicon-play-circle');
        $('#'+play_id).addClass('glyphicon-pause');
    }


$('.play-button').on('click', setAudioState);


function showLockStatus(results) {

    for (var i=0; i<results.length; i++) {

        var lock_status = results[i]['lock_status']
        var ps_id = results[i]['ps_id']

        var lock_id = ps_id + '_lock'

        if (lock_status == true) {
            $('#'+lock_id).addClass('glyphicon-lock')
        }
    }
}


checkLockStatus() 

function checkLockStatus() {
    var ps_ids = []

    $.each($('.lock-status-col'), function() {
        ps_id = $(this).data('lock_id');
        ps_ids.push(ps_id);
    });

    ps_data = {'ps_ids': ps_ids};

    $.post('/check-lock-status',
            ps_data,
            showLockStatus
    );
}





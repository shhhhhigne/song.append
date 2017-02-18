


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
    
    // var state = evt.target.is_playing;



    // if (playing == false) {
    //     if (playing_id == id) {
    //         playing = true;

    //     }
    // }
}

$('.play-button').on('click', setAudioState);
// $('')


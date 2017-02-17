function populateDropDownOwned(playlist_info) {

    $.each($('.track-playlist-dropdown'), function() {
        song_id = $(this).data('tooltip')
        for (playlist_id in playlist_info) {
            var playlist_name = playlist_info[playlist_id];
        
            // console.log(`playlist name = ${playlist_name}`)

             newItem = $('<li>');
             newItemLink = $('<a>', {value: playlist_id,
                                    class: 'add-song-link'
            });

             $(newItemLink).data('song_id', song_id)

            // alert(song_id);
            $(newItemLink).on('click', function() { addSongToPlaylist($(this).data('song_id'), playlist_id);
            });
            newItem.append(newItemLink);

            newItemLink.text(playlist_name);
            newItem.addClass('dropdown-playlist');

            $(this).append(newItem)
        }
    });
}

function getOwnedPlaylists() {
    $.get('/get-user-owned-playlists',
          populateDropDownOwned);
}

getOwnedPlaylists();


function populateDropDownBelong(playlist_info) {

    $('.track-playlist-dropdown').append('<li role="separator" class="divider"></li>');
    $('.track-playlist-dropdown').append('<li class="dropdown-header owned-playlists">Belong to Playlists</li>')

    $.each($('.track-playlist-dropdown'), function() {
            // body...
        song_id = $(this).data('tooltip')
        for (playlist_id in playlist_info) {
            var playlist_name = playlist_info[playlist_id];
        
            newItem = $('<li>');
            newItemLink = $('<a>', {value: playlist_id,
                                    class: 'add-song-link'

            });

            $(newItemLink).data('song_id', song_id)

            // alert(song_id);
            $(newItemLink).on('click', function() { addSongToPlaylist($(this).data('song_id'), playlist_id);
            });


            newItem.append(newItemLink);
            newItemLink.text(playlist_name);
            newItem.addClass('dropdown-playlist');
            $(this).append(newItem);
    } 
            
    });
    
}

function getBelongingPlaylists() {
    $.get('/get-user-belonging-playlists',
        populateDropDownBelong);
}

getBelongingPlaylists();


function songAddedToPlaylistSuccess(results){
    console.log(results);

    if (results['already_in_playlist'] == false){
        if (results['status'] == 'active') {
            alert(`${results['song_name']} added to ${results['playlist_name']}`)
        }
        else {
            alert(`${results['song_name']} requested for ${results['playlist_name']}`)
        }
    }
    else {
        alert(`${results['song_name']} already in ${results['playlist_name']}`)

    }
}

function addSongToPlaylist(song_id, playlist_id) {


    songIds = {'song_id': song_id,
               'playlist_id': playlist_id
    };

    $.post('/add-song-to-playlist/' + song_id + '/' + playlist_id,
           songIds,
           songAddedToPlaylistSuccess
    );
}


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


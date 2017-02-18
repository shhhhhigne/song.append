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
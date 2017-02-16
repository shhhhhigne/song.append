function populateDropDownOwned(playlist_info) {

    $.each($('.track-playlist-dropdown'), function() {
        song_id = $(this).data('tooltip')
        for (playlist_id in playlist_info) {
            var playlist_name = playlist_info[playlist_id];
        
            // console.log(`playlist name = ${playlist_name}`)

             newItem = $('<li>');
             newItemLink = $('<a>', { href: '/add-song-to-playlist/'+song_id+'/'+playlist_id,
                                      value: playlist_id

            });
            newItem.append(newItemLink);

            newItemLink.text(playlist_name);
            newItem.addClass('dropdown-playlist');

            $('.track-playlist-dropdown').append(newItem)
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
        
            // console.log(`playlist name = ${playlist_name}`)

            

            // console.log('hellooooooooo')
            // console.log('song_id: ' + song_id);

            newItem = $('<li>');
            newItemLink = $('<a>', {href: '/add-song-to-playlist/' + song_id + '/' + playlist_id,
                                    value: playlist_id song_id,
                                    class: 'add-song-link'
            });

            newItem.append(newItemLink);

            newItemLink.text(playlist_name);
            newItem.addClass('dropdown-playlist');
           
            $('.track-playlist-dropdown').append(newItem);
        }
    });
    
}

function getBelongingPlaylists() {
    $.get('/get-user-belonging-playlists',
        populateDropDownBelong);
}

getBelongingPlaylists();



// function addSongToPlaylist(evt) {

//     evt.preventDefault()

//     console.log($(this))
//     link = 



//     // adderIds = {'song_id': }

// }


// $('.add-song-link').on('click', addSongToPlaylist)


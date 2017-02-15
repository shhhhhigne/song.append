function populateDropDownOwned(playlist_info) {

    for (playlist_id in playlist_info) {
        var playlist_name = playlist_info[playlist_id];
    
        console.log(`playlist name = ${playlist_name}`)

         newItem = $('<li>');
         newItemLink = $('<a>', { href: '/get-playlist/'+playlist_id,
                                  value: playlist_id

        });
        newItem.append(newItemLink);

        newItemLink.text(playlist_name);
        newItem.addClass('dropdown-playlist');

        $('.track-playlist-dropdown').append(newItem)
    }
}

function getOwnedPlaylists() {
    console.log('get all p')
    $.get('/get-user-owned-playlists',
          populateDropDownOwned);
}

getOwnedPlaylists();


function populateDropDownBelong(playlist_info) {

    $('.track-playlist-dropdown').append('<li role="separator" class="divider"></li>');
    $('.track-playlist-dropdown').append('<li class="dropdown-header owned-playlists">Belong to Playlists</li>')


    for (playlist_id in playlist_info) {
        var playlist_name = playlist_info[playlist_id];
    
        console.log(`playlist name = ${playlist_name}`)

         newItem = $('<li>');
         newItemLink = $('<a>', { href: '/get-playlist/'+playlist_id,
                                  value: playlist_id

        });
        newItem.append(newItemLink);

        newItemLink.text(playlist_name);
        newItem.addClass('dropdown-playlist');
       
        $('.track-playlist-dropdown').append(newItem)
    }
}

function getBelongingPlaylists() {
    console.log('get all p')
    $.get('/get-user-belonging-playlists',
          populateDropDownBelong);
}

getBelongingPlaylists();


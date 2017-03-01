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

            $(newItemLink).data('playlist_id', playlist_id)


            $(newItemLink).data('song_id', song_id)

            // alert(song_id);
            // $(newItemLink).on('click', function() { addSongToPlaylist($(this).data('song_id'), playlist_id, true);
            // });

            $(newItemLink).on('click', function() { 
                askOwner($(this).data('song_id'), $(this).data('playlist_id'));
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
    $('.track-playlist-dropdown').append('<li class="dropdown-header belong-playlists">Belong to Playlists</li>')

    $.each($('.track-playlist-dropdown'), function() {
            // body...
        song_id = $(this).data('tooltip')
        for (playlist_id in playlist_info) {
            var playlist_name = playlist_info[playlist_id];
        
            newItem = $('<li>');
            newItemLink = $('<a>', {value: playlist_id,
                                    class: 'add-song-link'

            });

            $(newItemLink).data('playlist_id', playlist_id)

            $(newItemLink).data('song_id', song_id)

            // alert(song_id);
            // console.log(song_id)
            // console.log(playlist_id)
            $(newItemLink).on('click', function() { 
                addSongToPlaylist($(this).data('song_id'), $(this).data('playlist_id'), false, false);
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
    // var alert = results['alert']
    var song_name = results['song_name']
    var playlist_name = results['playlist_name']

    var vote_status = results['vote_status']
    var user_alert = results['user_alert']
    var add_alert = results['add_alert']

    console.log(results)

    $.alert({
            // icon: 'glyphicon glyphicon-thumbs-up',
            title: `${song_name} ${add_alert} ${playlist_name}`,
            content: `${user_alert}`
        });

    // alert(`${song_name} ${add_alert} ${playlist_name} \n ${user_alert}`)
    
}


function askOwner(song_id, playlist_id) {
    var override = $.confirm({ title: 'Override?',
            content: 'Would you like to suggest this song or simply add it',
            buttons: {
                add: function () {
                    var lock = $.confirm({ title: 'Lock?',
                            content: 'Would you like to lock this song in the playlist?',
                            buttons: {
                                Yes: function (){
                                    // console.log(song_id)
                                    // console.log (playlist_id)
                                    addSongToPlaylist(song_id, playlist_id, true, true);
                                    
                                },
                                No: function (){
                                        addSongToPlaylist(song_id, playlist_id, true, false)
                                                                    }
                            } 
                        });
                },
                suggest: function () {
                        addSongToPlaylist(song_id, playlist_id, true, true);
                    // action: function () {
                    //     addSongToPlaylist(song_id, playlist_id, false, false);
                    // }
                }
            }
        });
}


function addSongToPlaylist(song_id, playlist_id, override, lock) {

    // var os = 'not overriden'
    // var ls = 'unlocked'
    // if (override == true) {
    //     os = 'overriden'
    // }
    // if (lock == true) {
    //     ls = 'locked'
    // }
    // alert(song_id + ' ' +  playlist_id  + ' ' +   os  + ' ' +   ls)


    songIds = {'song_id': song_id,
               'playlist_id': playlist_id,
               'override': override,
               'lock': lock
    };

    $.post('/add-song-to-playlist/' + song_id + '/' + playlist_id,
           songIds,
           songAddedToPlaylistSuccess
    );
}
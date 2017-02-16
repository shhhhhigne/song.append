$(document).ready(function () {
  $(".nav li").removeClass("active");//this will remove the active class from  
                                     //previously active menu item
  var currentPage = $('.current-page').attr('value');

  var navCurrent = '#nav-'+currentPage;

  $(navCurrent).addClass('active');

});

var audioPlayer;
var playing_id;
var playing = false; 

var x

// TODO: make click and hold play pop up menu and single click play preview
function setAudioState() {
    x = event
    var evt = event;

    if (audioPlayer == null) {
        audioPlayer = new Audio();
    }

    if (playing_id != null && playing_id != evt.target.id) {
        // $('#playing_id').removeClass('is_playing');

        $('#'+playing_id).removeClass('glyphicon glyphicon-pause')
        $('#'+playing_id).removeClass('glyphicon glyphicon-play-circle')
    }

    $('#'+evt.target.id).addClass('glyphicon glyphicon-pause')

    // var state = evt.target.is_playing;



    // if (playing == false) {
    //     if (playing_id == id) {
    //         playing = true;

    //     }
    // }
}

$('.play-button').on('click', setAudioState);
// $('')

function populateDropDownOwned(playlist_info) {

    for (playlist_id in playlist_info) {
        var playlist_name = playlist_info[playlist_id];
    
        // console.log(`playlist name = ${playlist_name}`)

         newItem = $('<li>');
         newItemLink = $('<a>', { href: '/get-playlist/'+playlist_id,
                                  value: playlist_id

        });
        newItem.append(newItemLink);

        newItemLink.text(playlist_name);
        newItem.addClass('dropdown-playlist');

        $('#dropdown-playlist-menu').append(newItem)
    }
}

function getOwnedPlaylists() {
    $.get('/get-user-owned-playlists',
          populateDropDownOwned);
}

getOwnedPlaylists();


function populateDropDownBelong(playlist_info) {

    $('#dropdown-playlist-menu').append('<li role="separator" class="divider"></li>');
    $('#dropdown-playlist-menu').append('<li class="dropdown-header owned-playlists">Belong to Playlists</li>')


    for (playlist_id in playlist_info) {
        var playlist_name = playlist_info[playlist_id];
    
        // console.log(`playlist name = ${playlist_name}`)

         newItem = $('<li>');
         newItemLink = $('<a>', { href: '/get-playlist/'+playlist_id,
                                  value: playlist_id

        });
        newItem.append(newItemLink);

        newItemLink.text(playlist_name);
        newItem.addClass('dropdown-playlist');
       
        $('#dropdown-playlist-menu').append(newItem)
    }
}

function getBelongingPlaylists() {
    $.get('/get-user-belonging-playlists',
          populateDropDownBelong);
}

getBelongingPlaylists();


function populateDropDownGroups(group_info) {
    // console.log('popu')

    // console.log(group_info)

    for (group_id in group_info) {
        var group_name = group_info[group_id];
    
        // console.log(`group name = ${group_name}`)

         newItem = $('<li>');
         newItemLink = $('<a>', { href: '/add-to-group/'+group_id,
                                  value: group_id

        });
         newItem.append(newItemLink);

         // newItemLink.createAttribute('href');


         // newItemLink.href = '/get-playlist/'+playlist_id;
         // newItemLink = newItem.append($('<a>', { href: '/get-playlist/'+playlist_id.href }));


    
        // newItem.addClass('nav-playlist-'+playlist['id'])

        newItemLink.text(group_name);
        newItem.addClass('dropdown-group');
        // newItemLink.attr('value') = playlist_id;
        // newItemLink.attr('href') = '/get-playlist/'+playlist_id;

       
        $('#dropdown-group-menu').append(newItem)
    }
}

function getGroups() {
    $.get('/get-user-belonging-groups',
          populateDropDownGroups);
}

getGroups();
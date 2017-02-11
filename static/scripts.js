$(document).ready(function () {
  $(".nav li").removeClass("active");//this will remove the active class from  
                                     //previously active menu item
  var currentPage = $('.current-page').attr('value');

  var navCurrent = '#nav-'+currentPage;

  $(navCurrent).addClass('active');

});



function populateDropDown(playlist_info) {

    for (var [name, value] of Iterator(playlist_info)) {
    
        var newItem = $('<li>');
        var newItemLink = newItem.append($('<a>'));


        console.log(value)
        console.log(name)
        // newItem.addClass('nav-playlist-'+playlist['id'])

    //     newItemLink.append();
    //     newItem.addClass('dropdown-playlist');
    //     newItemLink.attr('value') = playlist['id'];
    //     newItemLink.attr('href') = '/get-playlist/'+playlist['id'];
    }
}

function getAllPlaylists() {
    $.get('/get-all-playlists',
          populateDropDown);
}

getAllPlaylists();

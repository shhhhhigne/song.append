function showMore(results) {
    var tracks = results['tracks']

    for (var song_id in tracks) {
        var song = tracks[song_id]
        var artist_info = `<a href='artist-info/` + song['artists'][0]['artist_id'] + `'>` + song['artists'][0]['artist_name'] + `</a>`
        for (var i=1; i < song['artists'].length; i++) {
            console.log(song['artists'][i]['artist_id'])
            artist_info = artist_info + `, <a href='artist-info/` + song['artists'][i]['artist_id'] + `'>` + song['artists'][i]['artist_name'] + `</a>`

        }

        //The HTML that is added to create each new row that contains a result
        var new_row = `<tr>
            <td>
                <span class="dropdown">
                <span class="glyphicon glyphicon-play-circle dropdown-toggle playDropdown" id="` + song['id'] + `" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"></span>
                <ul class="dropdown-menu" aria-labelledby="playDropdown">
                    <li id="` + song['id'] + `-preview" class='play-button' data-tooltip="` + song['preview'] + `"><a>Play 30 sec Preview</a></li>
                    <li><a href="#">Play Full Song on Spotify</a></li>
                </ul> 
                </span>
            </td>
            <td><a href='track/` + song['id'] + `'>` + song['name'] + `</a></td>
            <td>
                ` + artist_info + `
            </td>
            <td><a href='album-info/` + song['album_id'] + `'>` + song['album_name'] + `</a></td>
            <td>
                <span class="dropdown">
                <span class="glyphicon glyphicon-circle-arrow-left dropdown-toggle" id="playlist-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true"></span>
                <ul class="dropdown-menu dropdown-menu-right track-playlist-dropdown" aria-labelledby="playlist-dropdown" data-tooltip="` + song['id'] + `">
                    <li><a href="/create-playlist">+ New Playlist</a></li>
                    <li role="separator" class="divider"></li>
                    <li class='dropdown-header owned-playlists'>Owned Playlists</li>
                </ul>
                </span>
            </td>
        </tr>
        `

        $(".table tbody").append(new_row);
    }
    var offset = $('#load-more').data("offset") + 10;       
    $('#load-more').data('offset', offset);
}


function loadMore(evt) {

    evt.preventDefault();

    var toLoad = $('#load-more')

    var offset = toLoad.data('offset');
    var user_input = toLoad.data('user_input');

    console.log(offset)
    console.log(user_input)

    load_info = {'offset': offset,
                 'user_input': user_input
    }

    $.get('/load-more-results',
           load_info,
           showMore
    );
}

$('#load-more').on('click', loadMore);


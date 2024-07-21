 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.autocomplete');
    var instances = M.Autocomplete.init(elems);
  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.datepicker');
    var instances = M.Datepicker.init(elems);
  });

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
  });

document.addEventListener('DOMContentLoaded', function() {
  const addGameUrl = "{{ add_game_url }}";
  const searchInput = document.getElementById('game-search');
  const gameResults = document.getElementById('game-results');
  // Function to fetch games from the server
  async function fetchGames(query = '') {
    const response = await fetch(`/api/games?query=${query}`);
    return await response.json();
  }

 function renderGames(games) {
    gameResults.innerHTML = '';
    if (games == 0){
       const gameCard =`
        <div>
          <a href="/add_game">
            <div class="card">
              <div class="row card-image">
              </div>
              <i class="col offset-m6 m12 s12 l12 fa-solid fa-plus"></i>
              <div class="card-content">
                <p class="center-align">Add game to database</p>
              </div>
            </div>
          </a>
        </div>
`;
       gameResults.innerHTML = gameCard;
     }
    else{
    games.forEach(game => {
        const gameCard = `
        <div>
          <a href="/game_detail/${game.game_id}" class="card-link">
            <div class="card">
              <div class="card-image">
                <img src="${game.image_url}">
                  ${renderGameButton(game)}
              </div>
              <div class="card-content">
                <h4 class="center-align">${game.game_title}</h4>
                  <p><b>Developer: </b>${game.developer}</p>
                  <p><b>Publisher: </b>${game.game_publisher}</p>
                  <p><b>Release date: </b>${formatDate(game.release_date)}</p>
                  <p><b>Genre: </b>${game.genre}</p>
              </div>
            </div>
          </a>
        </div>
        `;
        gameResults.innerHTML += gameCard;
    });
    // Reinitialize Materialize tooltips
    var elems = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(elems, {});
     }}

function renderGameButton(game) {
    if (!isUserAuthenticated) {
        return '';
    }
    if (inMyGames.includes(game.game_id)) {
        return `
            <span class="btn-floating tooltipped halfway-fab waves-effect waves-light green"
                data-position="left"
                data-tooltip="in My Games">
                <i class="material-icons">check</i>
            </span>
        `;
    } else {
        return `
            <form action="/add_library/${game.game_id}" method="POST"> 
                <button type="submit" class="btn-floating tooltipped halfway-fab waves-effect waves-light red" 
                    data-position="left"
                    data-tooltip="add to My Games">
                    <i class="material-icons">add</i>
                </button>
            </form>
        `;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB'); // This will format the date as dd/mm/yyyy
}
  // Handle search input
searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    if (query) {
      fetchGames(query).then(renderGames);
  } else {
  renderGames([]);
     }
  });
});

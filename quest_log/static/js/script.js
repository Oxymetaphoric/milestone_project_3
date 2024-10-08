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
    try {
      const response = await fetch(`/api/games?query=${query}`);
      if (!response.ok) throw new Error('Network response was not ok');
      if (typeof searchInput === null){
         return []
       }
      return await response.json();
    } catch (error) {
      console.error('Error fetching games:', error);
      return [];
    }
  }

if (searchInput == null){
     return ''
   } else{
  // Handle search input //
  searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    if (query) {
      fetchGames(query).then(renderGames);
    } else {
      renderGames([]);
    }
  });
}

  function renderGames(games) {
    gameResults.innerHTML = '';
    if (games.length === 0) {
      const gameCard = `
        <div class="s8 m6 offset-m3 offset-s2">
          <a href="/add_game">
            <div class="card linkcard green" id="add_game">
              <div class="col s6 offset-s3 center-align">
                <i class="fa-solid fa-plus"></i>
              </div>
              <div class="card-content">
                <p class="center-align">Add game to database</p>
            </div>
          </a>
        </div>
      `;
      gameResults.innerHTML = gameCard;
    } else {
      let gameCardsHTML = '';
      games.forEach(game => {
        const gameCard = `
          <div>
            <a href="/game_detail/${game.game_id}" class="card-link">
              <div class="card linkcard">
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
        gameCardsHTML += gameCard;
      });
      gameResults.innerHTML = gameCardsHTML;

      // Reinitialize Materialize tooltips
      var elems = document.querySelectorAll('.tooltipped');
      M.Tooltip.init(elems, {});
    }
  }

  function renderGameButton(game) {
    if (typeof isUserAuthenticated === 'undefined' || typeof inMyGames === 'undefined') {
      console.error('isUserAuthenticated or inMyGames is not defined.');
      return '';
    }

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
    return date.toLocaleDateString('en-GB');
  }
});

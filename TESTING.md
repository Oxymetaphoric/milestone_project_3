## :microscope: Testing

---

### Testing Procedure

### Functional testing

| Test                                           | verified |
| ---------------------------------------------- | -------- |
| sign-up allows new users | yes |
| signup forces unique usernames | yes |
| login allows existing users to login | yes |
| login enforces correct password | yes | 
| Games page displays entire catalogue | yes | 
| search function triggers on each keystroke | yes |  
| Game cards link to appropriate gaem page | yes | 
| clicking the plus icon adds game to users My Games | yes | 
| icon displays tick if game is in My Games and reverts to a plus if removed | yes |
| games can be added to and removed from My Games | yes | 
| flash messages display correctly | yes |
| reviews can be added, deleted and edited | yes | 
| user profile displays edit box if user owns profile | yes | 
| users cannot edit profiles of others | yes | 
| My Reviews displays all users reviews | yes | 
| user accounts can be deleted | yes | 
| user account details can be edited | yes | 
| logout functionality works correctly | yes | 

### User Stories Testing


#### - First Time User Stories Testing

1. I want to encounter a landing page that succinctly and clearly explains the functionality of the site
    


2. I want to be able to browse review of games I am interested in

first time users can browse the catalogue of games and view the reviews of any games without he need for sign-up, and are presented with the catalogue of games immedietely on page load. 

3. As a first time user I want to be able to sign up to the site in order to login and start posting reviews 

The signup page is clearly signposted in the navigation of the page 

4. As a first time user I want to be able navigate the site easily and intuitively 

The site is simple and intuitive to navigate. Navigation elements are obvious and accessible at all screen sizes. Pages are clearly labelled, and functionality is explained through the use of tooltips and big, chunky UI elements. 

#### - Returning User Stories Testing

1. I want to be able to login quickly and easily
2. I want to be able to intuitively find all my prior reviews
3. I want to be able to delete reviews I have previously written
4. I want to be able to view the profiles of others 
5. I want to be able to write new reviews
6. I want to be able to add games to the database if they are not currently there

### HTML/CSS/JS/Python Validators

#### HTML

Using the W3 HTMl validator for my main page: 

![W3 HTML Validatior results](docs/html_validation.png)

#### CSS

uploading the CSS file to the W3 CSS validator:

![W3 CSS validator results](docs/css_validation.png)

### python / javaScript

using codeQL through github gave the following results: 

 ![codeQL](docs/CodeQL.png) 

### Lighthouse Testing

#### Desktop

##### Login

![login](docs/lighthouse/desktop/desktop_login.png)

##### Register

![register](docs/lighthouse/desktop/desktop_register.png)

##### Games

![main page](docs/lighthouse/desktop/desktop_games.png)

##### Add Game

![add gane](docs/lighthouse/desktop/desktop_add_game.png)

##### Game Detail

![game detail](docs/lighthouse/desktop/desktop_game_detail.png)

##### Edit Game

![edit game](docs/lighthouse/desktop/desktop_edit_game.png)

##### My Games

![my games](docs/lighthouse/desktop/desktop_my_games.png)

##### My Reviews

![my reviews](docs/lighthouse/desktop/desktop_my_reviews.png)

##### Edit Review

![edit review](docs/lighthouse/desktop/desktop_edit_review.png)

##### Profile

![profile](docs/lighthouse/desktop/desktop_profile.png)

#### Mobile 

##### Login

![login](docs/lighthouse/mobile/mobile_login.png)

##### Register

![register](docs/lighthouse/mobile/mobile_register.png)

##### Games

![main page](docs/lighthouse/mobile/mobile_games.png)

##### Add Game

![add gane](docs/lighthouse/mobile/mobile_add_game.png)

##### Game Detail

![game detail](docs/lighthouse/mobile/mobile_game_detail.png)

##### Edit Game

![edit game](docs/lighthouse/mobile/mobile_edit_games.png)

##### My Games

![my games](docs/lighthouse/mobile/mobile_my_games.png)

##### My Reviews

![my reviews](docs/lighthouse/mobile/mobile_my_reviews.png)

##### Edit Review

![edit review](docs/lighthouse/mobile/mobile_edit_review.png)

##### Profile

![profile](docs/lighthouse/mobile/mobile_profile.png)



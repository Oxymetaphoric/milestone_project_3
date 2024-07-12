# Milestone Project :three:

[LIVE SITE]()

![amiresponsive screenshot]()

---

## :world_map: Strategy

---

### Project Goals


This is my milestone two project for the [Code Institute's](http://www.codeinstitute.net/) *'Level 5 Diploma in Web Application Development'*. The goal of this project is to *Design, develop and implement a Back end for a web application using Python and a micro-framework.* To this end I am building a webapp utilising Flask & postgreSQL, that will alow users to create, modify, and track reviews for video games. The app will be aimed at gamers, people who are invested in tracking their relationship with videogames and offer a place for users to conveniently archive and keep a track of all the games that they have played and the thoughts that they had on them. Reviews will be abel to be tagged as public or private, and other visitors to the site will be able to browse reviews by game or by user. The site will also aggregate scores of reviews allowing users to accurately assess potential new purchases.  

#### User Goals

- browse the database of reviews 
- a place to keep track of games played
- get more information on unplayed games 

#### Site Operator Goals

- provide a reliable and secure platform for potential monetization through affiliate links 
- provide a good UX to enable growth of the userbase and accuracy of scores and breadth of database

#### Developer Goals

- develop further skill working with postgres and Flask
- develop a site that satisfies goals of the user and site operator and fulfils the project goals 
- create a good UX for users 
- build a performant and efficient site that has room for extensibility

---

## :earth_africa: Scope

---

### User Experience

#### Front End 

The site will be styled using the materialise toolkit to provide a consistent and aesthetic UI. I will use template inheritance using Jinja and Flask in order to create pages that have a consistent and accessible layout with minimal code to ensure a good UX. 

#### Back end 

I will utilise postgreSQL to build the moultiple tables within the database that will be necessary. These models will be: 


| Game | Data Type | Constraints | Key | Nullable |
|-------------|-----------|-------------|-----|----------|
| game_id | int | AUTO_INCREMENT | PK | No |
| title | varchar(255) | | | No |
| publisher | varchar(255) | | | Yes |
| developer | varchar(255) | | | Yes |
| release_date | date | | | Yes |
| genre | varchar(100) | | | Yes |
| image_url | varchar(512) | | | Yes |

| Review | Data Type | Constraints | Key | Nullable |
|-------------|-----------|-------------|-----|----------|
| review_id | int | AUTO_INCREMENT | PK | No |
| game_id | int | | FK (Game) | No |
| user_id | int | | FK (User) | No |
| content | text | | | No |
| hours_played | float | | | No |
| completed | bool | | | No |
| rating | int | CHECK (rating BETWEEN 1 AND 10) | | No |
| created_at | datetime | CURRENT TIMESTAMP | | No |

| User | Data Type | Constraints | Key | Nullable |
|-------------|-----------|-------------|-----|----------|
| user_id | int | AUTO_INCREMENT | PK | No |
| username | varchar(50) | UNIQUE | | No |
| email | varchar(255) | UNIQUE | | No |
| password_hash | varchar(255) | | | No |
| location | varchar(255) | | | Yes |
| created_at | datetime | DEFAULT CURRENT_TIMESTAMP | | No |

| UserGame | Data Type | Constraints | Key | Nullable |
|-------------|-----------|-------------|-----|----------|
| user_id | int | | PK, FK (User) | No |
| game_id | int | | PK, FK (Game) | No |
| added_at | datetime | DEFAULT CURRENT_TIMESTAMP | | No |

#### Target Audience

- video game players

#### User Requirements and Expectations

- easy and intiuitive navigation 
- secure login procedures 
- accessible 
- able to browse review by catagory (game, author, aggregate score etc. )
- able to write, delete, edit reviews 

#### User Stories

##### - First Time User

1. As a first time user I want to encounter a landing page that succinclty and clearly explains the functionality of the site 
2. As a first time user I want to be able to brwose review of games I am interested in
3. As a first time user I want to be able to sign up to the site in order to login and start posting reviews 
4. As a first time user I want to be able navigate the site easily and intuitively 

##### - Returning User

1. As a returning visitor I want to be able to login quickly and easily
2. As a returning visitor I want to be able to intuitively find all my prior reviews
3. As a returning visitor I want to be able to delete reviews I have previously written
4. As a returning visitor I want to be able to view the profile of others 
5. As a returning visitor I want to be able to write new reviews
6. As a returning visitor I want to be able to edit games to the database if they are not currently there


#### Identified tasks/needs the website should fulfill

| Features                                  |      Importance (1 -5) |
|----------------------------------------------|-------------------|
| site is easy to navigate ||
| site is responsive ||
| browsing the collection of games | |
| browsing all reviews of a given game ||
| user profiles that can be securely logged in to ||
| user profiles allow viewing/manipulation of existing reviews   | |
| allow users to edit games to the database  ||
| profile pages for each user, detailing reviews and some user stats (no. of reviews etc.)    ||
| site is accessible  ||
| site stores user information securely  ||
| site sends useers to a 404 with links to home if game/review/user not found ||
| search existing games   ||


#### Accessibility



---

## :bricks: Structure;

---

base.html
signup.html
login.html
user_profile.html
games.html
game.html
add_game.html
edit_game.html
delete_game.html
edit_review.html
delete_review.html
add_review.html
404.html



---

### Wireframes

#### Desktop Wireframes

#### Mobile Wireframes


### Features


---

## :art: Surface

---

### Design

#### Typography


#### Colour Palettes


### Technologies and Tools used

#### Languages

#### Tools

- **[Google Chrome](https://www.chrome.com/)**
- **[Firefox](https://www.firefox.com)**
- **[git](https://git-scm.com/)**
- **[VSCode for linux](https://code.visualstudio.com/)**
- **[GitHub](https://www.github.com)**
- **[Pencil](https://pencil.evolus.vn/)**
- **[Coolors](https://coolors.co/)**
- **[Google Fonts](https://fonts.google.com/)**
- **[Photopea](https://www.photopea.com/)**
- **[hextorgba](https://rgbacolorpicker.com/hex-to-rgba)**
- **[amiresponsive](https://ui.dev/amiresponsive)**

---

## :microscope: Testing

---


### Testing Procedure

### Functional testing

| test                                           | verified |
| ---------------------------------------------- | -------- |


### User Stories Testing

#### - First Time User Testing


#### - Returning User Testing


#### - Site Owner Testing


### Desktop

### HTML/CSS Validators

### WAVE

### Lighthouse

---

### Mobile Testing


### Bug fixes

--------------------------------
--------------------------------
--------------------------------
--------------------------------
--------------------------------


## :loudspeaker: Deployment

---

---

## :heart: Credits and Acknowledgments

---

My wonderful family!

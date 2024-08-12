# TO DO

- [x] remove add game button from main page
- [x] add redirect to search function. such that game not found redirects to add_game
- [x] format dates on 'games' page
- [x] add superuser functionality
- [x] restrict removing games to superuser
- [x] add ability to remove games from My Games
- [x] links for users to view the profile of others by clicking reviews they have written
- [x] move write reviews / remove game buttons to under game card in game_detail
- [x] profile stats
- [x] format dates in profile correctly
- [x] links in profile to a users library and reviews
- [x] consistent site-wide styling
    - [x] fonts
    - [x] background image?
    - [x] header
    - [x] flash messages
- [x] sort layout on All Games
- [x] remove ability for unauthenticated users to delete games
- [x] testing - add CodeQL screenshot
- [x] remove edit/delete review buttons from My Reviews if user is not the creator
- [x] fix delete game route
- [ ] add ability for users to 'like' reviews 
- [ ] 'add game to library' checkbox on adding game to database
- [ ] highest, lowest and average score given by users
- [ ] an avatar picker with some dummy examples to choose from hosted in static


## submission feedback

Learning Objective 1: Design, develop and implement a Back end for a web application using Python and a microframework.

- [x] add facility to delete account  
accounts can now be deleted by the account owner via the Profile page 

- [x] add a more obvious way to add games to site  
due to the unique nature of games t he database needs to be queried before a new gam can be added, which is the rationale for only presenting the user with the Add Game button when they have searched for a game and it doesn't already exist in the db 

- [x] size images  
done

- [x] more user feedback  
More visual feedback, flash feedback and alerts added across the site 

- [x] design work, colours/images  
Site has had a visual overhaul since initial submission, as documented in README

L02 – Model and manage data  

- [x] describe data scheme fully in readme  
Expanded on and fleshed out the previous descriptions  

- [x] add ERD  
ERD is available in the README beneath the text description of the database  
can be found here: (ERD)[docs/database_schema.png]  

L03: Query and manipulate data  

- [x] add a button to add new games to database   
addressed above  

- [x] prevent users from accesing accounts of others by URL manipulation  
users may not edit reviews or accounts that they do not own  

LO4: Deploy a Full Stack web application to a Cloud platform.  

- [x] detail the deployment process  
see README  

LO5: Identify and apply security features  

- [x] finish rationale and user stories   
fleshed out and expanded on User Stories 

- [x] credits  
updated  

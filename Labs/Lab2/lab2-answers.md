# Question 4
## a. 
Theaters-screening, screening-ticket,
## b. 
Theater name can change so yes
## c. 
movie
## d. 
ticket_id is invented

# Qusetion 6
theaters(_theater_name_, capacity)
screenings(_start_time_, /_theater_name_/, /imdb_key/)
movies(_imdb_key_, title, production_year, running_time)
tickets(_ticket_id_, /start_time/, /theater_name/, /username/)
customers(_username_, name, password)

# Question 7
## Solution 1:
Theater capacity - size of ticket table

Pros: Now data is accidentaly erased; few updates in table; 
Cons: Not contiunaly updated perhaps


## Solution 2: 
A table  attributes entry with number of availible seats in screening which updates every time a ticket is sold

Pros: No need to check size of ticket table, countinously updated
Cons: Need to update attribute, no history since data is erased which can lead to problems






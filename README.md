# Fetch-Search_user_Tweets
This project fetches recent tweets by user_name and stores them into database.  we can serach tweet details by search string on tweet text.

Requirments and Description:
1. This project is implemented using Python pyramid web framework, need it installed
2. It uses postgres as database. create databse by name 'twitter_db' in your database:
       On Linux: psql -Upostgres -c "create database twitter_db"
       
3. use database.sql file for creating tables:
      On Linux: psql -Upostgres -dtwitter_db -f database.sql
      
4. python's 'twitter' library is used for accessing Twiteer API's, that can be installed as follow:
      On Linux: pip3 install python-twitter

5. will need twitter API Access keys and secrets for accessing API's, put same in tweeter_credentails.py file.
6. once all set up is done, run python file main.py, that will start application running on port 8080


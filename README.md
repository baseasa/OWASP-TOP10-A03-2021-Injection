OWASP TOP 10 

# A03:2021-Injection #

This is a simple web application I built using Pyton (Flask) and SQLite to show
how SQL Injection (SQLi) attacks work.

The goal of this project is to show why input validation and parameterized queries
are critical for web security.

hOw To HacK iT ? 

If you know the credentials you can log in normally,

BUT...

You can bypass the password check completely without knowing any credentials.

If you type admin' --  in the username field and leave the password field blank
(or type something else, it doesn't matter), you will be logged in as the admin 
user and see the secret token.

WHY DOES THIS HAPPEN?

In the code the SQL query is constructed using a Python f-string :

sql_query = f"SELECT * FROM staff WHERE username = '{input_user}' 
AND password = '{input_pass}'"

When you input admin' -- the query becomes : 

SELECT * FROM staff WHERE username = 'admin' --' AND password = '...'

The -- in SQL signifies a comment. Everything after it is ignored by the database.
So, the query becomes 'select the user named admin' and ignores the password check.


## Django Real Estate Project 

#### technologies I use: 
* Django 
* Postgres 
* Redis 
* Gunicorn
* Whitenoise
* Heroku 
* Kaveh negar

#### [Live Project](https://kapar.herokuapp.com/) 
but phone verification doesn't work! because heroku need credit cart info for Redis

## for run project in local 
clone project 

`git clone https://github.com/theycallmereza/real-estate-ad.git`

Create .env file ( .env-example )

run 

`pipenv install` 
for install dependencies

if you want use phone validation 

`http://locahhost:8000/users/phone-varification`

you must run 

`redis-server`

don't forget 

`python manage.py migrate`
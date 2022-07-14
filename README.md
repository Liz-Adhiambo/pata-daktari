# Pata Daktari

Pata Daktari is an application where you can quickly book a doctor when in an emergency.Be able to view doctors availability and schedule visits to a doctor from the comfort of your home. Users can also find medical related blogs.



## Getting Started

To get a copy of Pata Daktari running locally on your end, you can:

1. Clone this repository, by running git clone then:

for ssh:
```
git@github.com:Liz2222/pata-daktari
```

or for https: 
```
https://github.com/Liz2222/pata-daktari
```

2. Set up a python environment to run the application:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install Django
```

### Prerequisites

Before you begin running the application, you must first install all the dependencies listed in the requirements.txt file.

```
 (venv) $ pip install -r requirements.txt

```

### Installing

1. Create a database:
  ```
(venv) $ psql CREATE DATABASE *DATABASE_NAME*;
(venv) $ pip install psycopg2

```

2. Create a new .env file and set up the following configurations:

 * Database name, host, password and user.

3. Make your first migrations: 


```
(env) $ python manage.py migrate 
```


4. Make migrations for the core application: 

```
(env) $ python manage.py makemigrations core
(env) $ python manage.py migrate
```
5. Create a super user / admin:


```
(env) $ python manage.py createsuperuser
```


## Built With

* Python3.8 - Backend

* Django4 - Python Framework

* PostgreSQL - Database 

* Heroku - Deployment

## User Stories:
**As as doctor, you can be able to:**
*  Sign up/sign in to the application.
*  Upon signing in, see a list of booked appointments
*  Upload a medical related blog to the website
* Get access to posted blogs,update or delete your blogs.

**As as patient, you can be able to:**

*  Sign up/sign in to the application.
* Upon login, book appointments and labtests
* Your booked appointment/labtest will be confirmed through an email notification 
* As soon as you book an appointment, you will be able to see the list of booked appointments and labtests on your profile page.

## BDD

| Behaviour | Input | Output |
| :---------------- | :---------------: | ------------------: |
| Load the page | **Choose** to login or sign up, as a docor or a patient | Login / Sign up page. User your credentials to access the application|
|Patients: View available doctors|Book Appointment or labtest | Upon success, a confirmation email is sent to the users email|
|Doctorss: Update their profile and speciality,Add medical related blogs|View added blogs ,update or delete them| View patients who have booked appointments with you| 

# Contributors:
* [Liz2222](https://github.com/Liz2222/)
* [gladys-gg](https://github.com/gladys-gg/)
* [christine-nkatha](https://github.com/christine-nkatha/)
* [Clement Lumumba](https://github.com/Clemo97)
* [lydiah1wachira](https://github.com/lydiah1wachira)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

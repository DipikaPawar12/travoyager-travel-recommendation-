<h1 align = "center">
    Travoyager- travel recommendation  system
</h1>

---

<img alt="PyPI - Python Version" src="https://img.shields.io/badge/python%20vesion-3.7.4-green"> <img alt="PyPI - Django Version" src="https://img.shields.io/badge/django%20version-3.0.6-blue">

<p>
<img src = "main.png">
</p>

<h1>Table of Content</h1>

- [Introduction](#introduction)
- [Technology Stack](#technology-stack)
- [Installations and Running](#installations-and-running)
- [Contributors](#contributors)



## Introduction

---
Hodophiles are the people who love to travel to new places, get to know different people and live everlasting experiences. These people often travel to random different places as their hobby or their routine. Most of the people in our country love to travel to multiple places at a time either for rest and relaxation purposes or tourist places. While people love travelling, planning for a trip can be a tedious task and one has to plan for the destination, mode of travel, hotel accommodation, what places to visit, how many days to spend etc. all in a decided budget. People may require to flip through numerous pages of brochures of travel agencies looking for the perfect plan for their trip. Many times the travel agencies packages seem costly to many people due to which they change their plans of travelling and decide to go on their own. Sometimes travelling on one’s own self can be a difficult task for finding hotels, restaurants, places to visit etc. We aim to create our own one-stop solution to all the travel arrangement problems.


## Technology Stack

---

- HTML/CSS/JavaScript
- Bootstrap
- Django
- Sqlite3

## Installations and Running

---

- Clone this repository

  ```
  git clone https://github.com/DipikaPawar12/travoyager-travel-recommendation-
  ```

- If you are not going to use Sqlite3 Database, change the DATABASES variable in settings.py file accordingly. You can Refer to [Django documentation](https://docs.djangoproject.com/en/3.0/ref/databases/)

- Please Don't forgot to add the <strong> Email </strong> and <strong>Password </strong> in <strong> settings </strong> file from which you want to send confirmation mail or visitor pass mail. Path to the settings file is <strong> visitor_manage/visitor_manage/settings.py </strong>

- Also add your own API key in the location.html file and path to the file is <strong>visitor_manage/src/templates/src/location.html </strong>

- Make Initial Migrations

  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```

- Run the Website on LocalHost
  ```
  python3 manage.py runserver
  ```
- All the necessary document are uploaded in the [folder](https://github.com/DipikaPawar12/travoyager-travel-recommendation-/tree/main/reports) for developing the software

Licensed under the [MIT License](LICENSE).

## Contributors

---
[Dipika Pawar](https://github.com/DipikaPawar12)| [Aanshi Patwari](https://github.com/aanshi18)| [Mansi Dobariya](https://github.com/mansi-ctrl)| [Nirva Sangani](https://github.com/nirvasangani)| [Meet Pedhadiya](https://github.com/MeeTP1310)| [Miracle Rindani](https://github.com/mrindani)| [Frency Chauhan](https://github.com/Frency-Chauhan)| [Bhumiti Gohel](https://github.com/bhumiti28)

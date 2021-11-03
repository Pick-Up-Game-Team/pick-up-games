# <h1 align="center">Pick Up Games 👋
    
![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
![HTML5](https://img.shields.io/badge/-HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS5](https://img.shields.io/badge/-CSS3-1572B6?style=flat-square&logo=css3)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-563D7C?style=flat-square&logo=bootstrap)
![Heroku](https://img.shields.io/badge/-Heroku-430098?style=flat-square&logo=heroku)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github)

> Pick Up Games is a web app wherein individuals can casually find local pick up games for their favorite sports. The web app allows users to view a map of the most popular local sports locations and match up with other players in the area. Supported sports will include basketball, soccer, tennis, and more.
> - Easy and convenient ✔️  
> - For everyone to meet up with other people who want to play pick up sports games! ⚽ ⚾ 🏀 🏉	 


## **Features in progess**✨

### Iteration 2
- [x] Homepage
- [x] Login page
- [x] User profile page
- [x] Account management
- [x] Registration page
- [x] Basic front-end testing

### Iteration 3
- [ ] Deployment
- [ ] Map
- [ ] Multiple sport support 

## **How It Works**⚡
To run this software, install the latest version of Python 3 [here](https://www.python.org/downloads/).
Then:
1. Clone this repo.
2. Inside the repo, a virtual environment using `py -m venv venv` (Windows) or `python3 -m venv venv` (Mac OS/Linux)
3. Activate the virtual environment with `venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Mac OS/Linux). On Windows machines, it may be necessary to enable scripts by running PowerShell as Administrator and entering `set-executionpolicy unrestricted`.
4. Install dependencies with `pip install -r requirements.txt`
5. In the same directory as `settings.py`, create a file named `config.py` and enter this line in the file: `SECRET_KEY = '<secret_key>'` where `<secret_key>` can be any string. The secret key used in production is not shared on GitHub for security purposes.
6. Update the database with `python manage.py makemigrations` and then `python manage.py migrate`.
7. Run the server with `python manage.py runserver`.

The server can be accessed locally at http://localhost:8000/.

To create an admin user, use `python manage.py createsuperuser`. The admin panel can be accessed at http://localhost:8000/admin.


> **The website is now deployed and live at** [Insert Website Here](https://youtu.be/dQw4w9WgXcQ)  !

- You are welcomed with a home page which will showcase features and services provided by the web application.
- You are able to log into your account with a username and password. You are able to register for a new account if they do not already have one.
- Your account is protected with a certain level of verification and authentication. 
- You are able to manage the personal information belonging to my account profile. This includes: name, location, profile picture, sports preferences, match record and ELO score visibility (future release).
- More features will be added.

## Running Test Suite 🖥️

- [Selenium](https://www.selenium.dev/) - We use Selenium for our front-end testing. The tool helps with automating web applications for workflow, prompt, login/logout section, and other testing purposes. Back-end testing is done with the Django test suite, which integrates with Selenium.
  To run tests, run this command in your terminal:
    ```python
    python manage.py test
    ```




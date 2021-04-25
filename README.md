# String Pulling Monitor Lite

![Project Flayer](https://github.com/LyonLee190/StringPullingMonitorLite/blob/main/doc/SPT%20Flyer.png)

<br />

> Links

- [Video Intro](https://www.youtube.com/watch?v=PjfuTH70crM)
- [Project Documentations](https://github.com/LyonLee190/StringPullingMonitorLite/tree/main/doc)
- [Wiring Schematic](https://github.com/LyonLee190/StringPullingMonitorLite/tree/main/doc/Wiring_Schematic.pdf)
- [Webserver Demo with Random Generated Data](https://github.com/LyonLee190/StringPullingMonitorLite/tree/Ang)

<br />

## How to use it

```bash
$ # The following commands are required to initialize the program.
$ # Get the code
$ git clone https://github.com/LyonLee190/StringPullingMonitorLite
$ cd StringPullingMonitorLite
$
$ # Virtualenv modules installation (Optional)
$ # We recommend to create virtualenv for each project avoiding module version conflicts.
$ # It is not mandatory especially when Raspberry Pi is used for single purpose.
$ virtualenv env
$ # Active virtualenv
$ source env/bin/activate
$ # Deactivate virtualenv once finishing tasks
$ deactivate
$
$ # Install modules
$ pip3 install -r requirements.txt
$
$ # The following commands are required
$ # to start the program.
$ # Active virtualenv
$ source env/bin/activate
$ # Set the FLASK_APP environment variable
$ export FLASK_APP=run.py
$
$ # Set up the DEBUG environment (Optional)
$ export FLASK_ENV=development
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=127.0.0.1 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

> Note: To use the app, please access the registration page and create a new user.
> After authentication, the app will unlock the private pages.

> Useful Links for Setting Up Raspberry Pi

- [The Official Site](https://www.raspberrypi.org/)
- [Connect Raspberry Pi through VNC Viewer](https://maker.pro/raspberry-pi/projects/how-to-connect-a-raspberry-pi-to-a-laptop-display)

<br />

> App / Base Blueprint

The *Base* blueprint handles the authentication (routes and forms) and assets management.
The structure is presented below:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- home/                                # Home Blueprint - serve app pages (private area)
   |    |-- base/                                # Base Blueprint - handles the authentication
   |         |-- static/
   |         |    |-- <css, JS, images>          # CSS files, Javascript files
   |         |
   |         |-- templates/                      # Templates used to render pages
   |              |
   |              |-- includes/                  #
   |              |    |-- navigation.html       # Top menu component
   |              |    |-- sidebar.html          # Sidebar component
   |              |    |-- footer.html           # App Footer
   |              |    |-- scripts.html          # Scripts common to all pages
   |              |
   |              |-- layouts/                   # Master pages
   |              |    |-- base-fullscreen.html  # Used by Authentication pages
   |              |    |-- base.html             # Used by common pages
   |              |
   |              |-- accounts/                  # Authentication pages
   |                   |-- login.html            # Login page
   |                   |-- register.html         # Registration page
   |
   |-- requirements.txt                          # Development modules - SQLite storage
   |-- requirements-mysql.txt                    # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt                    # Production modules  - PostgreSql DMBS
   |
   |-- .env                                      # Inject Configuration via Environment
   |-- config.py                                 # Set up the app
   |-- run.py                                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

> App / Home Blueprint

The *Home* blueprint handles UI Kit pages for authenticated users. This is the private zone of the app - the structure is presented below:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- base/                     # Base Blueprint - handles the authentication
   |    |-- home/                     # Home Blueprint - serve app pages (private area)
   |          |
   |          |-- templates/          # UI Kit Pages
   |              |
   |              |-- index.html      # Default page
   |              |-- page-404.html   # Error 404 page
   |              |-- page-500.html   # Error 500 page
   |              |-- page-403.html   # Error 403 page
   |              |-- *.html          # All other HTML pages
   |          |-- routers.py          # Webserver Class - render webpages & handle user requests
   |          |-- manager.py          # Hardware Manager Class - multiprocessing
   |          |-- hardware_manager.py # Hardware Manager Class - hardware interactions
   |          |-- hx711.py            # Load cell driver
   |          |-- Motor.py            # Step motor driver
   |-- requirements.txt               # Development modules - SQLite storage
   |-- requirements-mysql.txt         # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt         # Production modules  - PostgreSql DMBS
   |
   |-- .env                           # Inject Configuration via Environment
   |-- config.py                      # Set up the app
   |-- run.py                         # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

## Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The official website
- [Datta Able Flask](https://appseed.us/admin-dashboards/flask-dashboard-dattaable) - Webserver Template

<br />

---
[String Pulling Monitor Lite](https://github.com/LyonLee190/StringPullingMonitorLite/) - Designed by [LyonLee190](https://github.com/LyonLee190), [lovettxh](https://github.com/lovettxh), [Feiniu6ABC](https://github.com/Feiniu6ABC), and [cccrrrccc](https://github.com/cccrrrccc).

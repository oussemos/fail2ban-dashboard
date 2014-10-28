fail2ban-dashboard
==================

Fail2ban web dashboard written with Flask framework


### Quick Start

1. Clone the repo
  ```
  $ git clone https://github.com/oussemos/fail2ban-dashboard.git
  $ cd fail2ban-dashboard
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python home.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

### Deployment 

For more stability, you can deploy the application with Gunicorn.

  ```
  $ pip install gunicorn
  $ gunicorn home:app -p fail2ban_dashboard.pid -b 0.0.0.0:5000 -D
  ```

### Issues

* The application is still under development, don't hesitate to give advice, open an <a href="https://github.com/oussemos/fail2ban-dashboard/issues">issue</a> or contribute.

### ToDO List

* Using AJAX to get informations and updates
* Possibility to modify filters 


### System

* This app was developed and tested under Debian Wheezy


### Screenshots

![Home](docs/screenshots/home.png)

![Config](docs/screenshots/config.png)

![Banned IP](docs/screenshots/banned.png)

### Changelog

(28-10-2014)

* Filters configuration
* Authentification with password

### Author

<a href="http://oussema.cherni.tn">Oussema Cherni</a> (@<a href="http://twitter.com/oussemos">oussemos</a> on Twitter)

### License

Open source licensed under the MIT license.




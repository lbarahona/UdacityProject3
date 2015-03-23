# UdacityProject3: Item Catalog

This project is part of of Udacity's [Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004).

### Description

As described in the project description for the course, the project consists in develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.


### Running the project

The project can be excuted using Vagrant, you'll have to navigate to the `vagrant/` folder and execute the command `vagrant up`.
To run the test cases follow this steps:

optional step: put your own github application key information into the config.py file and ensure http://localhost:5000 is your github application callback.  A temporary one is included already for testing purposes and at least at the time this is submitted it is an active key.

- `vagrant ssh`(To login to the VM).
- `cd /vagrant/item_catalog`(To navigate to the project directory).
- Run `python flask_app.py`(To navigate to the project directory). The database will be created if this is the first time the application has been run and default data will be insterted for demo purposes.
- After you see "Running on http://0.0.0.0:5000/" in the shell, open a browser to http://localhost:5000
- You're now ready to navigate to the application.

Note: if you log out the application, you'll not be able to edit the data.
Also, If you do not use the included Vagrant environment you will also need to install the following Python libraries:

* bleach
* github-flask
* dicttoxml

###API endpoints

The following API endpoints are provided within the application:

JSON: http://localhost:5000/company/(company-id)/JSON
XML: http://localhost:5000/company/(company-id)/XML

example: http://localhost:5000/company/1/JSON


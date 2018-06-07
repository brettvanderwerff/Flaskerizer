# Flaskerizer


[![Build Status](https://travis-ci.org/brettvanderwerff/Flaskerizer.svg?branch=master)](https://travis-ci.org/brettvanderwerff/Flaskerizer)

## What is the Flaskerizer and what problem does it solve?

Bootstrap templates from websites like https://Bootstrapmade.com/ and https://startBootstrap.com are a fast way to get very dynamic website up and running, but Bootstap templates typically don't work "out of the box" with the python web framework Flask and require some tedious directory building and broken link fixing before being functional with Flask. This is especially true if the Bootstrap templates are for large multi-page websites. 

The Flaskerizer automates the necessary directory building and link creation needed to make Bootstrap templates work "out of the box" with Flask. The Flaskerizer also automatically creates a python script with the appropriate routes and basic error handling needed to serve the Bootstrap template as a Flask app.

The Flaskerizer takes a Bootstrap template that looks like this "out of the box" with Flask:

![picture alt](/readme_images/not_working_example.png)

and converts it to something that looks like this "out of the box" with Flask:

![picture alt](/readme_images/working_example.png)

## Dependencies

Flask: 0.12.1 or higher

## Setup and Operation

1. Clone the repo to your computer

2. Install dependencies by opening a terminal in top level directory of the repo and entering `$ pip install -r requirements.txt` 

3. Download your favorite Bootstrap template from https://Bootstrapmade.com/ .Note that there is an example template (Alstar_example) that you can use if you don't want to download one. 

4. If the Bootstrap template is downloaded as a zipped file you will need to unzip the Bootstrap template

5. Open the Configuration file(`config.py`) and:

* set value of key *templates_path* to the full path of the folder containing the HTML files of the Bootstrap template you downloaded. Note that there may be multiple folders that contain HTML files, generally you want to set the 'templates_path' value equal to the path of the folder with the *most* HTML files in it (see config.py for example).

* set value of key *static_path* to the full path of the folder containing the css, javascript, images, etc. folders of the Bootstrap template you downloaded (see config.py for example).

* set value of key *javascript_path* to the full path of the folder specifically containing the javascript files of the Bootstrap template you downloaded (see config.py for example).

 
6. Run the program by opening a terminal in the top level directory of the repo and entering `$ python flaskerizer.py` (this may vary slightly by environment)

7. After running flaskerizer.py, clear your browser's cache and enter `$ python Flaskerized_app/app.py` in the terminal to launch the newly made Flask app.

8. View your website by opening the browser to your local address on port 5000 (i.e. http://127.0.0.1:5000 / http://0.0.0.0:5000) , Note: may have to enter http://127.0.0.1:5000/index.html / http://0.0.0.0:5000/index.html to route the  website homepage.

- **NOTE :** You may need to clear your browser's cache to view the website properly (I'm not sure why this happens sometimes)

- **WARNING :** Do not delete the *Alstar_example* template example from the directory. It is used to run tests.

## For a Docker Version
Docker using alpine 3.7, Python 3.6, uwsgi and Nginx

1. Run steps 1 to 6 above

3. Navigate to the Flaskerized_app directory

2. Run `docker build -t SOMETAG .`

3. Run `docker run -d -p 5000:80 --name TESTDOCKER SOMETAG`

4. Run step 8 above

## How it works

The Flasker has two main classes:
* `StructureDirectory()`

* `WriteApp()`

**The StructureDirectory class**

The StructureDirectory class makes the typical Flask project folder structure in the Flaskerized_app directory. This includes making a 'static' folder that will contain all the front end files from the Bootstrap template (css, javascript, etc.) and a 'templates' folder that will contain all the HTML files from the Bootstrap template. The StructureDirectory class takes both the full path to Bootstrap template HTML files (templates_path) and the full path to the css, javascript, images, etc. folders of the Bootstrap template (static_path) as arguments.  

The StructureDirectory class has 3 main methods:

`migrate_static`:

The migrate_static method creates a 'static' folder in the Flaskerized_app directory. All the folders from the designated 'static_path' (see config.py) of the Bootstrap template will be copied to the newly made 'static' folder in the Flaskerized_app directory. The assumption is made that all folders in the Bootstrap template contain the front end information that belongs in the 'static' folder like css, javascript, images, etc. This may not always be the case, but often it is. 

`parse_html`:

The parse_html method creates a 'templates' folder in the Flaskerized_app directory. The string content of all the HTML files from the designated 'templates_path' (see config.py) of the Bootstrap template are parsed for any links that references the content placed in the 'static' folder by the migrate_static method. If any links are found, they are modified to reflect the correct structure of the Flask application. This avoids broken links that would otherwise incorrectly reference files in the 'static' folder. Once the HTML files are parsed and corrected, they are written to the newly made 'templates' folder in the Flaskerized_app directory.

`parse_javascript`:

Similar to the parse_html method, the parse_javascript method iterates through the string content of all the javascript files from the designated 'javascript_path' (see config.py) of the Bootstrap template in search of links that reference the content placed in the 'static' folder by the migrate_static method. If any links are found, they are modified to reflect the correct structure of the Flask application. Once the javascript files are parsed and corrected, they are written to the newly made 'static' folder in the appropriate subdirectory of the Flaskerized_app folder.

**The WriteApp class**


The WriteApp class has one main method:

`write_app`:

The write_app method automatically writes a python script 'app.py' with the necessary instructions to launch a Flask app of the Bootstrap template. This method writes the import statements, instantiates the 'app' object from the Flask class, and writes a main loop to run the app. This method also detects the HTML files in the 'templates' folder and writes the corresponding routes to these HTML files. If any of the HTML files are named for an HTTP status code, the write_app method generates an error handling route for that file. This assumes that any HTML file with an HTTP status code in it's name reflects an error, which is usually true. 


## Contribution Guidelines

1. Comment on an issue you would like assigned to you. 
2. Fork the Flaskerizer repo onto your github.
3. Clone your fork to your machine.
4. Use git to make a new branch on your local machine by opening a terminal and typing `$ git checkout -b XXXX-SHORT_TITLE_OF_ISSUE` where XXX is the zero padded issue number, such as 0001. For example: `$ git checkout -b 0001-HTTP_STATUS_CODE_ISSUE` would be good for the first issue in the repo. 
5. Make a pull request right away by pushing your branch to github and trying to merge your fork with my master branch. It's okay if you have not made any progress, just title the pull request whatever you titled the branch and add 'Work in progress" to the title so that I know you are working on it. 
6. Let me know when you are done with your branch and we can review the code together before finalizing the contribution :)

### Running the tests

Tests have been written for StructureDirectory and WriteApp classes and status_code_to_word function: 

This app uses unittest for unit testing.

You can also use [nose2](https://nose2.readthedocs.io/en/latest/) for running all the tests at once. Run `pip install nose2`  and then in the main directory run `nose2` to run the tests.

## Contributors:

A list of people that have contributed to Flaskerizer by completing a pull request:

- [Mayank Nader](https://github.com/makkoncept)

- [@jmbriody](https://github.com/jmbriody)

- [@PvtHaggard](https://github.com/PvtHaggard)

- [@WeepingJarl012](https://github.com/WeepingJarl012)

- [@etiontdn](https://github.com/etiontdn)

- [@heberfabiano](https://github.com/eberfabiano)







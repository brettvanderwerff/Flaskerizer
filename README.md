# Flaskerizer

## What is the Flaskerizer and what problem does it solve?

Bootstrap templates from websites like https://bootstrapmade.com/ and https://startbootstrap.com/ are a fast way to get very dynamic website up and running, but bootstap templates typically don't work "out of the box" with the python web framework Flask and require some tedious directory building and broken link fixing before being functional with Flask. This is especially true if the bootstrap templates are for large multi-page websites. 

The Flaskerizer automates the necessary directory building and link creation needed to make Bootstrap templates work "out of the box" with Flask. The Flaskerizer also automatically creates a python script with the appropriate routes and basic error handling needed to serve the bootstrap template as a Flask app.

The Flaskerizer takes a bootstrap template that looks like this "out of the box" with Flask:

![picture alt](/readme_images/not_working_example.png)

and converts it to something that looks like this "out of the box" with Flask:

![picture alt](/readme_images/working_example.png)

## Dependencies

Flask: 0.12.1 or higher

## Setup and Operation

1. Clone the repo to your computer
2. Install dependencies by opening a terminal in top level directory of the repo and entering `$ pip install -r requirements.txt` 
3. Download your favorite bootstrap template from https://bootstrapmade.com/ and https://startbootstrap.com/. Note that there are two example templates in the repo (Folio_example and startbootstrap-freelancer-template) from https://bootstrapmade.com/ and https://startbootstrap.com/ respectively that you can use if you don't want to download one. This program was designed only with templates from https://bootstrapmade.com/ in mind and though it also works with many templates from https://startbootstrap.com/, I would love to extend the flexibility of the program to work well with other bootstrap template sources (see issues) 
4. Open the Configuration file(`config.py`) and set value of key *directory_path* to the full path of the bootstrap template you downloaded (or use the example template in the repo).
5. Run the program by opening a terminal in the top level directory of the repo and entering `$ python flaskerizer.py` (this may vary slightly by environment)
6. After running flaskerizer.py, enter `$ python app.py` in the terminal to launch the newly made Flask app from the app.py file.
7. View your website by opening the browser to your local address on port 5000 (i.e. http://127.0.0.1:5000 / http://0.0.0.0:5000) , Note: may have to enter http://127.0.0.1:5000/index.html / http://0.0.0.0:5000/index.html to route the  website homepage.
8. You may need to clear your browser's cache to view the website properly (I'm not sure why this happens sometimes)

- **NOTE :** Do not delete the *Folio_example* template example from the directory. It is used to run tests.

## For a Docker Version
Docker using alpine 3.7, Python 3.6, uwsgi and Nginx

1. Run steps 1 to 5 above
2. Run `docker build -t SOMETAG .`
3. Run `docker run -d -p 5000:80 --name TESTDOCKER SOMETAG`
4. Run steps 7 to 8 above

## How it works

The Flasker has two main classes:
* `StructureDirectory()`

* `WriteApp()`

**The StructureDirectory class**

The StructureDirectory class makes the typical Flask project folder structure in the top level directory of the repo. This includes making a 'static' folder that will contain all the front end files from the bootstrap template (css, javascript, etc.) and a 'templates' folder that will contain all the HTML files from the bootstrap template. The StructureDirectory class takes the directory of the bootstrap template as an argument. 

The StructureDirectory class has two main methods:

`migrate_static`:

The migrate_static method creates a 'static' folder in the top level directory of the repo. All the folders from the bootstrap template directory will be copied to the newly made 'static' folder in the top level directory of the repo. The assumption is made that all folders in the bootstrap template contain the front end information that belongs in the 'static' folder like css, javascript, images, etc. This may not always be the case, but I think often it is. 

`parse_html`:

The parse_html method creates a 'templates' folder in the top level directory of the repo. The string content of all the HTML files in the top level directory of the bootstrap template then parsed for any links that references the content placed in the 'static' folder by the migrate_static method. If any links are found, they are modified to reflect the correct structure of the Flask application. This avoids broken links that would otherwise incorrectly reference files in the 'static' folder. Once the HTML files are parsed and corrected, they are written to the newly made 'templates' folder in the top level directory of the repo. 

**The WriteApp class**


The WriteApp class has one main method:

`write_app`:

The write_app method automatically writes a python script 'app.py' with the necessary instructions to launch a Flask app of the bootstrap template. This method writes the import statements, instantiates the 'app' object from the Flask class, and writes a main loop to run the app. This method also detects the HTML files in the 'templates' folder and writes the corresponding routes to these HTML files. If any of the HTML files are named for an HTTP status code, the write_app method generates an error handling route for that file. This assumes that any HTML file with an HTTP status code in it's name reflects an error, which I think is usually true. 

## Running the tests

Tests have been written for StructureDirectory and WriteApp classes and status_code_to_word function: 

This app uses unittest and [nose](https://nose.readthedocs.io/en/latest/) for testing.

To run the tests open the terminal in the top level directory and enter `$ nosetests`, this will find and run all the test automatically. Make sure that you have `$ pip install -r requirements.txt`, as nose is an external dependency. 

## The Example Templates

Folio_example - A small one page bootstrap template from https://bootstrapmade.com/

startbootstrap-freelancer-template - A very popular bootsrap template with over 2000 forks and 1500 stars on github. It is downloaded from https://startbootstrap.com/

## Contribution Guidelines

1. Comment on an issue you would like assigned to you. 
2. Fork the Flaskerizer repo onto your github.
3. Clone your fork to your machine.
4. Use git to make a new branch on your local machine by opening a terminal and typing `$ git checkout -b XXXX-SHORT_TITLE_OF_ISSUE` where XXX is the zero padded issue number, such as 0001. For example: `$ git checkout -b 0001-HTTP_STATUS_CODE_ISSUE` would be good for the first issue in the repo. 
5. Make a pull request right away by pushing your branch to github and trying to merge your fork with my master branch. It's okay if you have not made any progress, just title the pull request whatever you titled the branch and add 'Work in progress" to the title so that I know you are working on it. 
6. Let me know when you are done with your branch and we can review the code together before finalizing the contribution :)

## Contributors:

A list of people that have contributed to Flaskerizer:

- [Mayank Nader](https://github.com/makkoncept)

- [@jmbriody](https://github.com/jmbriody)

- [@PvtHaggard](https://github.com/PvtHaggard)

- [@WeepingJarl012](https://github.com/WeepingJarl012)








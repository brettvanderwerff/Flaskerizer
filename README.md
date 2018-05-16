# Flaskerizer

==WORK IN PROGRESS==

## What is the Flaskerizer and what problem does it solve?

Bootstrap templates from websites like https://bootstrapmade.com/ are a fast way to get very dynamic website up and running, but Bootstap templates typically don't work "out of the box" with the python web framework Flask and require some tedious directory building and broken link fixing before being functional with Flask. 

The Flaskerizer automates the necessary directory building and link creation needed to make Bootstrap templates work "out of the box" with Flask. The Flaskerizer also automatically creates a python script with the appropriate routes needed to serve the Bootstrap template as a Flask app.

##Dependencies

Flask: 0.12.2 or higher

##Setup and Operation

1. Clone the repo to your computer
2. Install dependencies by opening terminal in top level directory and entering `pip install -r requirements.txt` 
3. Download your favorite bootstrap template from https://bootstrapmade.com/ (note that there are two example templates in the repo (Folio_example and Sailor_example) from https://bootstrapmade.com/ that you can use if you don't want to download one. 
4. Open flaskerizer.py and edit the 'directory' argument of the 'structure_directory_object' to include the full path of the bootstrap template you downloaded.
5. Run the program by opening a terminal in the top level directory of the repo and entering `$ python app.py` (this may vary slightly by environment)

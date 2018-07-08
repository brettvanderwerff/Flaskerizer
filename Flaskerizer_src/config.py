import Flaskerizer_src.Examples.Alstar_example as Example
import os

''' 
After unzipping your Bootstrap template, copy the path of the unzipped "top level" folder to the 'top_level_path' key
value in the CONFIGURATION dictionary below.
 
Open the template and find the folder that contains the HTML files. Copy the 
full path to this folder to the 'templates_path' key value in the CONFIGURATION dictionary below. These HTML files will 
eventually be migrated to the Flask 'templates' folder by Flaskerizer. 

Note that there is sometimes more than one folder containing HTML files in bootstrap templates. 
Choose the one folder that does not contain any rerouting HTML files (hint this folder will usually have the most 
HTML files in it). Also note that this 'templates_path' may simply be the top level directory of the bootstrap
template as it is in the 'Alstar_example'
 
'''

CONFIGURATION = {
       'top_level_path' : os.path.dirname(Example.__file__),
       'templates_path': os.path.dirname(Example.__file__)
}

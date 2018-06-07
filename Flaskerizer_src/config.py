import Flaskerizer_src.Examples.Alstar_example as Example
import os

''' 
After unzipping your Bootstrap template, open the template and find the folder that contains the HTML files. Copy the 
full path to this folder to the 'templates_path' key value in the CONFIGURATION dictionary below. These HTML files will 
eventually be migrated to the Flask 'templates' folder by Flaskerizer. 

Note that there is sometimes more than one folder containing HTML files in bootstrap templates. 
Choose the one folder that does not contain any rerouting HTML files (hint this folder will usually have the most 
HTML files in it). Also note that this 'templates_path' may simply be the top level directory of the bootstrap
template as it is in the 'Alstar_example'
 
Next find the folder within the Bootstrap template that contains all the css, javascript, images, etc. Copy the 
full path to this folder to the 'static_path' key value in the CONFIGURATION dictionary below. These HTML files will 
eventually be migrated to the Flask 'static' folder by Flaskerizer.

Note that this 'static_path' may also simply be the top level directory of the Bootstrap template as it is in the 
'Alstar_example'

Finally, find the folder within the Bootstrap template that specifically contains the javascript and copy the full path 
to this folder to the 'javascript_path' key value in the CONFIGURATION dictionary below.  
  
Currently the default 'templates_path', 'static_path', and 'javascript_path' key values are set to reflect paths
that are correct for the 'Alstar_example', you should replace these values with the paths to your unzipped 
Bootstrap template of choice. 
'''

CONFIGURATION = {
       'templates_path': os.path.dirname(Example.__file__),
       'static_path' : os.path.dirname(Example.__file__),
       'javascript_path' : os.path.join(os.path.dirname(Example.__file__), os.path.basename('js'))
}

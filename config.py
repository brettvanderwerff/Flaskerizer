import os

''' 
After unzipping your Bootstrap template, open the template and find the folder that contains the HTML files. Copy the 
full path to this folder to the 'templates_path' value in the COFIGURATION dictionary below. These HTML files will be 
migrated to the Flask 'templates' folder by Flaskerizer. 

Note that there is sometimes more than one folder containing HTML files in bootstrap templates. 
Choose the one folder that does not contain any rerouting HTML files (hint this folder will usually have the most 
HTML files in it). Also note that this 'templates_path' may simply be the top level directory of the bootstrap
template as it is in the 'Folio_example'
 
Next find the folder within the boostrap template that contains all the css, javascript, images, etc. Copy the 
full path to this folder to the 'static_path' value in the COFIGURATION dictionary below. These HTML files will be 
migrated to the Flask 'static' folder by Flaskerizer.

Note that this 'static_path' may also simply be the top level directory of the bootstrap template as it is in the 
'Folio_example'
  
Currently the default 'templates_path' and 'static_path' values are set to reflect paths
that are correcet for the 'Folio_example', you should replace these values with the paths to your unzipped 
Bootstrap template of choice. 
'''

CONFIGURATION = {
       'templates_path': os.path.join(os.getcwd(), os.path.basename('Folio_example')),
       'static_path' : os.path.join(os.getcwd(), os.path.basename('Folio_example'))
}

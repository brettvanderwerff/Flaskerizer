import os

''' 
enter the full path of downloaded bootstrap template as the value of directory_path key.
Currently 'Folio_example' is the default template and you can continue with it or replace it 
with the path of your downloaded bootstrap template 
'''

CONFIGURATION = {
       'directory_path': os.path.join(os.getcwd(), os.path.basename('Folio_example'))
}

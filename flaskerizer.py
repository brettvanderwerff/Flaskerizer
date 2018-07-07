'''
~~~~~~~~~~~~~~~~
The Flaskerizer
~~~~~~~~~~~~~~~~

A program for automating the development of Flask apps from Bootstrap templates. Run this file ('flaskerizer.py')
to begin the flaskerization process on the example template 'Alstar_example'. To change the Bootstrap template from
the default example to the template of your choice, please refer to the config.py file in the Flaskerizer_src directory.
'''
from Flaskerizer_src.config import CONFIGURATION
from Flaskerizer_src.structure_directory import StructureDirectory
from Flaskerizer_src.write_app import WriteApp

structure_directory_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'])
structure_directory_object.make_folders()
structure_directory_object.search_tree()
write_app_object = WriteApp()
write_app_object.write_app()



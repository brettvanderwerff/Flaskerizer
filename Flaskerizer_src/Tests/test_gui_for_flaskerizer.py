import unittest
import os
from Flaskerizer_src.gui_for_flaskerizer import ChooseFilesGUI

class TestGUI(unittest.TestCase):

    def setUp(self):
        '''Instantiates an object 'test' from the ChoseFilesGUI class.
        '''
        self.test = ChooseFilesGUI(True)

    def test_values(self):
        """Gets the default values from the html,
        static and js string variables in the ChooseFilesGUI. Then
        sets new ones and tests to see if they are fully
        functional.
        """
        self.assertEqual(self.test.get_values(),
                         ["Select one HTML file from the main HTML folder of the Bootstrap template",
                          "Select the 'top level' folder of the Bootstrap template"])
        self.test.templates_path.set("Templates Path Location")
        self.test.top_level_path.set("Top Level Path Location")
        self.assertEqual(self.test.get_values(),
                         ['Templates Path Location', "Top Level Path Location"])

    def test_path(self):
        """Gives two file paths to the path_to_folder function in ChooseFilesGUI
        and checks if it returns the folder path.
        """
        self.this_directory = os.path.dirname(os.path.abspath(__file__))
        self.path_to_folder = self.test.path_to_folder
        self.assertEqual(self.path_to_folder(self.this_directory + "/gui_for_flaskerizer.py"), (self.this_directory))
        self.assertEqual(self.path_to_folder(self.this_directory + "/flaskerizer.py"), (self.this_directory))


if __name__ == '__main__':
    unittest.main()

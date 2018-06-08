import unittest
import os
from Flaskerizer_src.gui_for_flaskerizer import ChooseFilesGUI

class TestGUI(unittest.TestCase):
    def test_values(self):
        """Gets the default values from the html,
        static and js string variables in the ChooseFilesGUI. Then
        sets new ones and tests to see if they are fully
        functional.
        """
        self.testclass = ChooseFilesGUI(True)
        self.assertEqual(self.testclass.get_values(),
         ["Select the main HTML file, usually a index.html file",
         "Select the folder that contains the css and img folders or the one with CSS and images files",
         "Select one JavaScript (.js) file from the template JavaScript folder"])
        self.testclass.html_location.set("Html Location")
        self.testclass.static_location.set("Static Location")
        self.testclass.js_location.set("JS Location")
        self.assertEqual(self.testclass.get_values(),
         ['Html Location', "Static Location",
         "JS Location"])

    def test_path(self):
        """Tests the path_to_folder function from ChooseFilesGUI
        gives it two files path uses the function
        and compares it to this directory path.
        """
        self.this_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_class = ChooseFilesGUI(True)
        self.path_to_folder = self.test_class.path_to_folder
        self.assertEqual(self.path_to_folder(self.this_directory + "/gui_for_flaskerizer.py"), (self.this_directory))
        self.assertEqual(self.path_to_folder(self.this_directory + "/flaskerizer.py"), (self.this_directory))


if __name__ == '__main__':
    unittest.main()

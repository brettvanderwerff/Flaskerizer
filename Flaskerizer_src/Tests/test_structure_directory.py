from Flaskerizer_src.config import CONFIGURATION
from Flaskerizer_src.structure_directory import StructureDirectory
import Flaskerizer_src.Examples.Alstar_example as Example
import Flaskerizer_src.Tests as Tests
import flaskerizer
import unittest
import os

class TestStructureDirectory(unittest.TestCase):
    maxDiff = None # reveals difference between test strings and "gold standard" strings

    def setUp(self):
        '''Instantiates an object 'test' from the StructureDirectory class.
        '''
        self.test = StructureDirectory(templates_path=CONFIGURATION['templates_path'],
                                       static_path=CONFIGURATION['static_path'],
                                       javascript_path=CONFIGURATION['javascript_path'])

    def test_mkdir(self):
        '''Tests that mkdir creates a folder named static and a folder named templates.
        '''
        self.test.mkdir('static')
        self.test.mkdir('templates')
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__), os.path.basename('static'))))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__), os.path.basename('templates'))))

    def test_migrate_static(self):
        '''Tests that migrate_static migrates the correct number of folders from the bootstrap template directory to
        the static directory of the Flask app.
        '''
        source_directory = os.path.dirname(Example.__file__)
        write_directory = os.path.join(os.path.dirname(flaskerizer.__file__), os.path.basename('static'))
        self.test.migrate_static()
        source_dir_list = []
        write_dir_list = []
        for folder in os.listdir(source_directory):
            if os.path.isdir(folder):
                source_dir_list.append(folder)
        for folder in os.listdir(write_directory):
            if os.path.isdir(folder):
                write_dir_list.append(folder)
        self.assertEqual(len(source_dir_list), len(write_dir_list))

    def test_parse_html(self):
        ''' Tests that parse_html creates a file 'index.html' in a templates folder that matches a "gold standard"
         version of 'index.html' called 'index_test_file.html'.
        '''
        self.test.migrate_static()         # to make all the tests independent. Tests are run in random order
        self.test.parse_html()
        html_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                        os.path.basename('templates'),
                                        os.path.basename('index.html'))
        with open(html_dir, 'r') as test_obj:
            test_string = test_obj.read()
        test_dir = os.path.join(os.path.dirname(Tests.__file__),
                                        os.path.basename('testing_files'),
                                        os.path.basename('index_test_file.html'))
        with open(test_dir) as gold_obj:
            gold_string = gold_obj.read()
        self.assertMultiLineEqual(test_string, gold_string)

    def test_parse_javascript(self):
        ''' Tests that parse_javascript creates a file 'custom.js' in the static/js folder that matches a
        "gold standard" version of 'custom.js' called 'custom_test_file.js'.
        '''
        self.test.migrate_static()
        self.test.parse_javascript()
        js_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                        os.path.basename('static'),
                                        os.path.basename('js'),
                                        os.path.basename('custom.js'))
        with open(js_dir, 'r') as test_obj:
            test_string = test_obj.read()
        test_dir = os.path.join(os.path.dirname(Tests.__file__),
                                        os.path.basename('testing_files'),
                                        os.path.basename('custom_test_file.js'))
        with open(test_dir) as gold_obj:
            gold_string = gold_obj.read()
        self.assertMultiLineEqual(test_string, gold_string)

if __name__ == "__main__":
    unittest.main()

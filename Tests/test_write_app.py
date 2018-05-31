from config import CONFIGURATION
import flaskerizer
import unittest
import os
from structure_directory import StructureDirectory
from write_app import WriteApp

class TestWriteApp(unittest.TestCase):
    maxDiff = None # reveals difference between test strings and "gold standard" strings

    def setUp(self):
        '''Instantiates a 'structure_directory_object' from the StructureDirectory class.The object 'test' is also instantiated from the
        WriteApp class.
        '''
        structure_directory_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'],
                                                        static_path=CONFIGURATION['static_path'],
                                                        javascript_path=CONFIGURATION['javascript_path'])
        structure_directory_object.migrate_static()
        structure_directory_object.parse_html()
        self.test = WriteApp()

    def test_get_routes(self):
        '''Tests that the get_routes method of the WriteApp class returns a list.
        '''
        self.assertIsInstance(self.test.get_routes(), list)

    def test_write_app(self):
        ''' Tests that write_app method of the WriteApp class creates a file app.py that matches a "gold standard"
        app.py called app_test_file.py from the testing_files directory. These two files are compared line for line
        in the test.
        '''
        self.test.write_app()
        with open('app.py', 'r') as test_obj:
            test_string = test_obj.read()
        test_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                os.path.basename('Tests'),
                                os.path.basename('testing_files'),
                                os.path.basename('app_test_file.py'))
        with open(test_dir) as gold_obj:
            gold_string = gold_obj.read()
        self.assertMultiLineEqual(test_string, gold_string)


if __name__ == '__main__':
    unittest.main()




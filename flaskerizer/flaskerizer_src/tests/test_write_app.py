import flaskerizer.flaskerizer_src.examples.Alstar_example as example
from flaskerizer.flaskerizer_src.structure_directory import StructureDirectory
from flaskerizer.flaskerizer_src.write_app import WriteApp
import flaskerizer.flaskerizer_src.tests as tests
import flaskerizer
import unittest
import os

class TestWriteApp(unittest.TestCase):
    maxDiff = None # reveals difference between test strings and "gold standard" strings
    def setUp(self):
        '''Instantiates a 'structure_directory_object' from the StructureDirectory class.The object 'test' is
        also instantiated from the WriteApp class. tests are written to test both cases where the config.py
        CONFIGURATION['large_app_structure'] is set to either True or False.
        '''
        structure_directory_object = StructureDirectory(templates_path=os.path.dirname(example.__file__),
                                                        top_level_path=os.path.dirname(example.__file__),
                                                        large_app_Structure=True)

        structure_directory_object.structure_directory()
        self.test = WriteApp()

    def test_get_routes(self):
        '''tests that the get_routes method of the WriteApp class returns a list.
        '''
        self.assertIsInstance(self.test.get_routes(), list)

    def test_write_app(self):
        '''When CONFIGURATION['large_app_structure'] == False, tests that write_small_app method of the WriteApp
        class creates a file 'app.py' that matches a "gold standard" app.py called app_test_file.py from the testing_files
        directory. These two files are compared line for line in the test. Similarly, when
        CONFIGURATION['large_app_structure'] == False, tests if the 'routes.py' file written by write_large_app matches
        a gold standard version.
        '''

        self.test.write_large_app()
        test_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                               os.path.basename('Test_application'),
                               os.path.basename('Test_application'),
                           os.path.basename('routes.py'))
        gold_dir = os.path.join(os.path.dirname(tests.__file__),
                                os.path.basename('testing_files'),
                                os.path.basename('routes_test_file.py'))
        with open(test_dir, 'r') as test_obj:
            test_string = test_obj.read()
        with open(gold_dir) as gold_obj:
            gold_string = gold_obj.read()
        self.assertMultiLineEqual(test_string, gold_string)


if __name__ == '__main__':
    unittest.main()





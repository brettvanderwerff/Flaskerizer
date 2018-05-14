import unittest
import os
from structure_directory import StructureDirectory
from write_app import WriteApp

class TestWriteApp(unittest.TestCase):
    def setUp(self):
        flaskerizer_object = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))
        flaskerizer_object.migrate_static()
        flaskerizer_object.parse_html()

    def test_get_routes(self):
        '''Tests that the get_routes function returns a list.
        '''
        test = WriteApp()
        self.assertIsInstance(test.get_routes(), list)

    def test_write_app(self):
        ''' Tests that write_app creates a file app.py that matches a "gold standard"  app.py called
        app_test_file.py from the testing_files directory. These two files are compared line for line.
        '''
        test = WriteApp()
        test.write_app()
        with open('app.py', 'r') as test_obj:
            test_string = test_obj.read()
        test_dir = os.path.join(os.getcwd(), os.path.basename('testing_files'), os.path.basename('app_test_file.py'))
        with open(test_dir) as gold_obj:
            gold_string = gold_obj.read()
        self.assertMultiLineEqual(test_string, gold_string)

if __name__ == '__main__':
    unittest.main()




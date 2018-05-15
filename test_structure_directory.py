import unittest
from structure_directory import StructureDirectory
import os

class TestStructureDirectory(unittest.TestCase):
    maxDiff = None # reveals difference between test strings and "gold standard" strings

    def setUp(self):
        '''Instantiates an object 'test' from the StructureDirectory class. The path to the Bootstrap
        template 'Folio' is given as an argument for testing purposes.
        '''
        self.test = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))

    def test_mkdir(self):
        '''Tests that mkdir creates a folder named static and a folder named templates.
        '''
        self.test.mkdir('static')
        self.test.mkdir('templates')
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), os.path.basename('static'))))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), os.path.basename('templates'))))

    def test_migrate_static(self):
        '''Tests that migrate_static migrates the correct number of folders from the bootstrap template directory to
        the static directory of the Flask app.
        '''
        source_directory = os.path.join(os.getcwd(), os.path.basename('Folio'))
        write_directory = os.path.join(os.getcwd(), os.path.basename('static'))
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
        ''' Tests that parse_html creates a file 'blog-grid.html' in a templates folder that matches a "gold standard"
         version of 'blog-grid.html' called 'blog-grid_test_file.html'.
        '''
        self.test.parse_html()
        html_dir = os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename('blog-grid.html'))
        with open(html_dir, 'r') as test_obj:
            test_string = test_obj.read()
        test_dir = os.path.join(os.getcwd(), os.path.basename('testing_files'), os.path.basename('blog-grid_test_file.html'))
        with open(test_dir) as gold_obj:
            gold_string = gold_obj.read()
        self.assertMultiLineEqual(test_string, gold_string)

if __name__ == "__main__":
    unittest.main()
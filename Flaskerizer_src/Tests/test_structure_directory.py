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
                                       top_level_path=CONFIGURATION['top_level_path'])


    def test_mkdir(self):
        '''Tests that mkdir creates a folder named static and a folder named templates. Also test that the subfolders
        of static "css, fons, img, and js" are created.
        '''
        self.test.mkdir()
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                    os.path.basename('Flaskerized_app'),
                                                    os.path.basename('static'))))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                    os.path.basename('Flaskerized_app'),
                                                    os.path.basename('static'),
                                                    os.path.basename('css'))))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                    os.path.basename('Flaskerized_app'),
                                                    os.path.basename('static'),
                                                    os.path.basename('fonts'))))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                    os.path.basename('Flaskerized_app'),
                                                    os.path.basename('static'),
                                                    os.path.basename('img'))))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                    os.path.basename('Flaskerized_app'),
                                                    os.path.basename('static'),
                                                    os.path.basename('js'))))
        self.assertTrue(os.path.exists(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                    os.path.basename('Flaskerized_app'),
                                                    os.path.basename('templates'))))

    def test_migrate_files(self):
        '''Tests that migrate_files migrates the correct number of files from the bootstrap template directory to
        the Flask app.
        '''
        migrate_dict = self.test.detect_static_files()
        self.test.migrate_files(migrate_dict)
        file_list = []
        extensions = ['.js', '.css', '.jpg', '.png', 'gif', '.ico', '.otf', '.eot', '.svg', '.ttf', '.woff', '.woff2']
        directory = os.path.join(os.path.dirname(flaskerizer.__file__),
                                 os.path.basename('Flaskerized_app'))
        for path, subdir, files in os.walk(directory):
            for name in files:
                for extension in extensions:
                    if name.endswith(extension):
                        file_list.append(name)
        self.assertEqual(135, len(file_list))



if __name__ == "__main__":
    unittest.main()

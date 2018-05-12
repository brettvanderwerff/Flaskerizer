import unittest
from structure_directory import StructureDirectory
import shutil
import os

#ToDo make test that validates parse html migrates all the html files to templates (assert length of file list) do the same for migrates static

class TestStructureDirectory(unittest.TestCase):
    def test_mkdir(self):
        '''Tests that mkdir creates a folder named static.
        '''
        test = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))
        test.mkdir('static')
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), os.path.basename('static'))))

    def test_migrate_static(self):
        '''Tests that migrate_static results in the generation of a folder names static.
        '''
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('static')))
        test = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))
        test.migrate_static()
        for item in os.listdir(os.path.join(os.getcwd(), os.path.basename('static'))):
            self.assertTrue(os.path.exists(
                os.path.join(os.getcwd(), os.path.basename('static'), os.path.basename(item))))

    def test_parse_html(self):
        '''Tests that migrate_static results in the generation of a folder names static.
        '''
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('templates')))
        test = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))
        test.parse_html()
        for item in os.listdir(os.path.join(os.getcwd(), os.path.basename('templates'))):
            self.assertTrue(os.path.exists(
                os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename(item))))

if __name__ == "__main__":
    unittest.main()
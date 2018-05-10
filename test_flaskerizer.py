import unittest
from flaskerizer import Flaskerizer
import shutil
import os

class TestFlaskerizer(unittest.TestCase):
    def test_mkdir(self):
        test = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
        test.mkdir('static')
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), os.path.basename('static'))))

    def test_migrate_static(self):
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('static')))
        test = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
        test.migrate_static()
        for item in os.listdir(os.path.join(os.getcwd(), os.path.basename('static'))):
            self.assertTrue(os.path.exists(
                os.path.join(os.getcwd(), os.path.basename('static'), os.path.basename(item))))

    def test_migrate_templates(self):
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('templates')))
        test = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
        test.migrate_templates()
        for item in os.listdir(os.path.join(os.getcwd(), os.path.basename('templates'))):
            self.assertTrue(os.path.exists(
                os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename(item))))



if __name__ == "__main__":
    unittest.main()
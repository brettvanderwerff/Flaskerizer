import io #needed to backport some open statements to python 2.7
import os
from Flaskerizer_src.config import CONFIGURATION
import flaskerizer
import shutil

class StructureDirectory():
    def __init__(self, templates_path, static_path, javascript_path):
        ''' The templates_path attribute of the StructureDirectory class is a path to the HTML
        files in the Bootstrap template source folder that will be migrated to the Flask 'templates' folder. The
        static_path attribute of the StructureDirectory class is a path to the css, javascript, images, fonts, etc.
        content of the Bootstrap template source folder that will be migrated to the Flask 'static' folder.
        '''
        self.templates_path = templates_path
        self.static_path = static_path
        self.javascript_path = javascript_path

    def mkdir(self, dir):
        '''Makes folder of dir name in the Flaskerized_app directory.
        '''
        dir_path = os.path.join(os.path.dirname(flaskerizer.__file__),
                                os.path.basename('Flaskerized_app'),
                                os.path.basename(dir))
        if not os.path.exists(dir_path):
            print('generating {} folder'.format(dir))
            os.makedirs(dir_path)
        else:
            print('overwriting old {} folder'.format(dir))
            shutil.rmtree(os.path.join(os.path.dirname(flaskerizer.__file__),
                                       os.path.basename('Flaskerized_app'),
                                       os.path.basename(dir)))
            os.makedirs(dir_path)

    def migrate_javascript(self, javascript_obj, file_name):
        '''Iterates through every line in the javascript files of the source Bootstrap template and
        adds /static/ to any line that should point to contents of the static folder of the flask app (i.e. lines that
        reference images in the 'static' folder)
        '''
        js_folder_name = os.path.basename(self.javascript_path)
        write_directory = os.path.join(os.path.dirname(flaskerizer.__file__),
                                       os.path.basename('Flaskerized_app'),
                                       os.path.basename('static'),
                                       os.path.basename(js_folder_name))
        with io.open(os.path.join(write_directory, file_name), 'w', encoding='utf-8') as write_obj:
            for line in javascript_obj.readlines():
                for folder in os.listdir(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                      os.path.basename('Flaskerized_app'),
                                                      os.path.basename('static'))):
                    if ('\"' + str(folder) + "/") in line:
                        split_line = line.split("\"" + str(folder) + "/")
                        line = ("\"" + 'static/' + (str(folder) + "/")).join(split_line)
                    elif ('\'' + str(folder) + "/") in line:
                        split_line = line.split("\'" + str(folder) + "/")
                        line = ("\'" + 'static/' + (str(folder) + "/")).join(split_line)
                write_obj.write(line)

    def parse_javascript(self):
        '''Locates all the javascript files in the Bootstrap template directory.
        '''
        for file_name in os.listdir(self.javascript_path):
            if '.js' in file_name:
                print('generating content for {} and migrating content to templates folder'.format(file_name))
                source_directory = os.path.join(self.javascript_path, os.path.basename(file_name))
                with io.open(source_directory, 'r', encoding='utf-8') as javascript_obj:
                    self.migrate_javascript(javascript_obj, file_name)

    def migrate_static(self):
        '''Makes a static folder then migrates all the folders from the bootstrap template directory that belong in
        the static folder (css, js, etc) to the newly made static folder.
        '''
        self.mkdir('static')
        for item in os.listdir(self.static_path):
            item_path = os.path.join(self.static_path, os.path.basename(item))
            if os.path.isdir(item_path):
                print('migrating {} to static folder'.format(item))
                shutil.copytree(item_path,
                                os.path.join(os.path.dirname(flaskerizer.__file__),
                                             os.path.basename('Flaskerized_app'),
                                             os.path.basename('static'),
                                             os.path.basename(item)))

    def migrate_templates(self, html_content, file_name):
        '''Iterates through every line in the html_content of an HTML document with the filename 'file_name' and
        adds /static/ to any line that should point to contents of the static folder of the flask app (i.e. lines that
        reference content of the css or javascript folder etc.).
        '''
        write_directory = os.path.join(os.path.dirname(flaskerizer.__file__),
                                       os.path.basename('Flaskerized_app'),
                                       os.path.basename('templates'),
                                       os.path.basename(file_name))
        for line in html_content:
            with io.open(write_directory, 'a') as write_obj:
                for folder in os.listdir(os.path.join(os.path.dirname(flaskerizer.__file__),
                                                      os.path.basename('Flaskerized_app'),
                                                      os.path.basename('static'))):
                    if ('=\"' + str(folder) + "/") in line or ('=\"../' + str(folder) + "/") in line:
                        split_line = line.replace('../', '').split("\"" + str(folder) + "/")
                        line = ("\"" + '/static/' + (str(folder) + "/")).join(split_line)
                    elif ('\"./' + str(folder) + "/") in line:
                        split_line = line.split("\"./" + str(folder) + "/")
                        line = ("\"./" + 'static/' + (str(folder) + "/")).join(split_line)
                write_obj.write(line)

    def parse_html(self):
        '''Locates all the HTML files in the Bootstrap template directory.
        '''
        self.mkdir('templates')
        for file_name in os.listdir(self.templates_path):
            if '.html' in file_name:
                print('generating content for {} and migrating content to templates folder'.format(file_name))
                source_directory = os.path.join(self.templates_path, os.path.basename(file_name))
                with io.open(source_directory, 'r') as html_content:
                    self.migrate_templates(html_content, file_name)

if __name__ == "__main__":
    my_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'],
                                   static_path=CONFIGURATION['static_path'],
                                   javascript_path=CONFIGURATION['javascript_path'])
    my_object.migrate_static()
    my_object.parse_html()
    my_object.parse_javascript()



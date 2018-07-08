import io #needed to backport some open statements to python 2.7
import os
from Flaskerizer_src.config import CONFIGURATION
from Flaskerizer_src.target_folders import target_folders
import flaskerizer
import random
import shutil

class StructureDirectory():
    def __init__(self, templates_path, top_level_path):
        '''
        The top_level_path attribute of the StructureDirectory class is a path to the top level folder
         of the Bootstrap template source folder. The templates_path attribute of the StructureDirectory class is a
         path to the HTML files in the Bootstrap template source folder that will be migrated to the Flask 'templates'
        folder.
        '''
        self.top_level_path = top_level_path
        self.templates_path = templates_path
        self.flaskerized_app_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                        os.path.basename('Flaskerized_app'))

    def mkdir(self):
        '''Makes folder of dir name in the Flaskerized_app directory.
        '''
        folders = {'templates': [''],
                   'static': ['js', 'css', 'img', 'fonts']
                   }
        for folder, subfolders in folders.items():
            for subfolder in subfolders:
                dir_path = os.path.join(self.flaskerized_app_dir,
                                        os.path.basename(folder),
                                        os.path.basename(subfolder))
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                else:
                    shutil.rmtree(dir_path)
                    os.makedirs(dir_path)


    def migrate_files(self, migrate_dict):
        '''Migration of all files detected by the detect_files method to their appropriate destinations in the
        Flaskerized_app directory (i.e. files with .css extension migrated to the css subfolder of the static folder.)
        '''
        for name in migrate_dict:
            item_extension = name.split('.')[-1]
            shutil.copyfile(migrate_dict[name]['source_dir'],
                            os.path.join(self.flaskerized_app_dir,
                                         os.path.basename(target_folders[item_extension]['folder']),
                                         os.path.basename(target_folders[item_extension]['subfolder']),
                                         os.path.basename(name)))
    def detect_static_files(self):
        '''Walks through the entire directory tree of the Bootstrap template detecting any files with extensions that
        are needed for the static content of the Flask app (i.e. .css, .js, .img, etc). The names and locations of
        these files are saved in a dictionary.
        '''
        migrate_dict = {}
        extensions = ['.js', '.css', '.jpg', '.png', '.ico', '.otf', '.eot', '.svg', '.ttf', '.woff', '.woff2']
        path = self.top_level_path
        for path, subdir, files in os.walk(path):
            for name in files:
                if name in migrate_dict:
                    duplicate_name = str(random.randint(1,100)) + name
                    for extension in extensions:
                        if name.endswith(extension):
                            migrate_dict[duplicate_name] = {'source_dir': '', 'link': ''}
                            migrate_dict[duplicate_name]['source_dir'] = os.path.join(path, name)
                            migrate_dict[duplicate_name]['link'] = os.path.join(path, name).replace('\\', '/')[
                                                         len(self.top_level_path) + 1:]
                    continue
                for extension in extensions:
                    if name.endswith(extension):
                        migrate_dict[name] = {'source_dir': '', 'link' : ''}
                        migrate_dict[name]['source_dir'] = os.path.join(path, name)
                        migrate_dict[name]['link'] = os.path.join(path, name).replace('\\',
                                                                                      '/')[len(self.templates_path) + 1:]
        return migrate_dict

    def detect_and_migrate_html_files(self):
        '''Detects files with the extension ".html" in the templates_path. These files are migrated to the "templates"
        folder of the Flaskerized_app directory.
        '''
        for file_name in os.listdir(self.templates_path):
            if file_name.endswith('.html'):
                shutil.copyfile(os.path.join(self.templates_path, os.path.basename(file_name)),
                                os.path.join(self.flaskerized_app_dir,
                                             os.path.basename('templates'),
                                             os.path.basename(file_name)))

    def file_list(self):
        '''Returns a list of JavaScript, CSS, and HTML files that need to be parsed for broken links by the
        "parse_links method.
        '''
        file_list = []
        for extension in ['html', 'js', 'css']:
            extension_dir = os.path.join(self.flaskerized_app_dir,
                                         os.path.basename(target_folders[extension]['folder']),
                                         os.path.basename(target_folders[extension]['subfolder']))
        for file in os.listdir(extension_dir):
            file_list.append(os.path.join(extension_dir, os.path.basename(file)))
        return file_list

    def parse_links(self, migrate_dict):
        '''Iterates through every file returned by the "file_list" method and
        adds /static/ to any line that should point to contents of the static folder of the flask app (i.e. lines that
        reference content of the css or javascript folder etc.).
        '''
        file_list = self.file_list()
        for file in file_list:
            line_list = []
            with io.open(file, 'r', encoding='utf-8') as read_obj: #there are encoding issues here
                for line in read_obj:
                    line_list.append(line)
            os.remove(file)
            with io.open(file, 'a', encoding='utf-8') as write_obj:
                for line in line_list:
                    for name in migrate_dict:
                        if migrate_dict[name]['link'] in line:
                            if name.endswith('.html'):
                                line = line.replace(migrate_dict[name]['link'], name)
                            else:
                                for extension in target_folders:
                                    if name.endswith(extension):
                                        line = line.replace(migrate_dict[name]['link'],
                                                            '/'.join((target_folders[extension]['folder'],
                                                                      target_folders[extension]['subfolder'], name)))
                    write_obj.write(line)

    def structure_directory(self):
        self.mkdir()
        migrate_dict = self.detect_static_files()
        self.migrate_files(migrate_dict)
        self.detect_and_migrate_html_files()
        self.parse_links(migrate_dict)


if __name__ == "__main__":
    my_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'],
                                   top_level_path=CONFIGURATION['top_level_path'])
    my_object.structure_directory()






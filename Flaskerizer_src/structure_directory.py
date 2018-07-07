import io #needed to backport some open statements to python 2.7
import os
from Flaskerizer_src.config import CONFIGURATION
import flaskerizer
import random
import shutil

class StructureDirectory():
    def __init__(self, templates_path):
        ''' The templates_path attribute of the StructureDirectory class is a path to the HTML
        files in the Bootstrap template source folder that will be migrated to the Flask 'templates' folder. The
        static_path attribute of the StructureDirectory class is a path to the css, javascript, images, fonts, etc.
        content of the Bootstrap template source folder that will be migrated to the Flask 'static' folder.
        '''
        self.templates_path = templates_path


    def mkdir(self, folder, subfolder):
        '''Makes folder of dir name in the Flaskerized_app directory.
        '''
        dir_path = os.path.join(os.path.dirname(flaskerizer.__file__),
                                os.path.basename('Flaskerized_app'),
                                os.path.basename(folder),
                                os.path.basename(subfolder))
        if not os.path.exists(dir_path):
            print('generating {} folder'.format(folder))
            os.makedirs(dir_path)
        else:
            print('overwriting old {} folder'.format(folder))
            shutil.rmtree(os.path.join(os.path.dirname(flaskerizer.__file__),
                                       os.path.basename('Flaskerized_app'),
                                       os.path.basename(folder),
                                       os.path.basename(subfolder)))
            os.makedirs(dir_path)

    def make_folders(self):
        folders = {'templates' : [''],
                   'static' : ['js', 'css', 'img', 'fonts']
                   }
        for folder, subfolders in folders.items():
            for subfolder in subfolders:
                self.mkdir(folder, subfolder)

    def migrate_files(self, migrate_dict):
        target_folders = {
            'html' : {'folder': 'templates',
                      'subfolder' : ''
                      },
            'js': {'folder': 'static',
                      'subfolder' : 'js'
                   },
            'css': {'folder': 'static',
                      'subfolder' : 'css'
                    },
            'jpg': {'folder': 'static',
                      'subfolder' : 'img'
                    },
            'png': {'folder': 'static',
                      'subfolder' : 'img'
                    },
            'ico': {'folder': 'static',
                      'subfolder' : 'img'
                    },
            'otf': {'folder': 'static',
                      'subfolder' : 'fonts'
                    },
            'eot': {'folder': 'static',
                      'subfolder' : 'fonts'
                    },
            'svg': {'folder': 'static',
                      'subfolder' : 'fonts'
                    },
            'ttf': {'folder': 'static',
                      'subfolder' : 'fonts'
                    },
            'woff': {'folder': 'static',
                      'subfolder' : 'fonts'
                    },
            'woff2': {'folder': 'static',
                      'subfolder' : 'fonts'
                    },
        }
        for name in migrate_dict:
            item_extension = name.split('.')[-1]
            shutil.copyfile(migrate_dict[name]['source_dir'],
                            os.path.join(os.path.dirname(flaskerizer.__file__),
                                         os.path.basename('Flaskerized_app'),
                                         os.path.basename(target_folders[item_extension]['folder']),
                                         os.path.basename(target_folders[item_extension]['subfolder']),
                                         os.path.basename(name)))



    def search_tree(self):
        migrate_dict = {}
        extensions = ['.html', '.js', '.css', '.jpg', '.png', '.ico', '.otf', '.eot', '.svg', '.ttf', '.woff', '.woff2']
        path = self.templates_path
        for path, subdir, files in os.walk(path):
            for name in files:
                if name in migrate_dict:
                    duplicate_name = str(random.randint(1,100)) + name
                    for extension in extensions:
                        if name.endswith(extension):
                            migrate_dict[duplicate_name] = {'source_dir': '', 'link': ''}
                            migrate_dict[duplicate_name]['source_dir'] = os.path.join(path, name)
                            migrate_dict[duplicate_name]['link'] = os.path.join(path, name).replace('\\', '/')[
                                                         len(self.templates_path) + 1:]
                    continue
                for extension in extensions:
                    if name.endswith(extension):
                        migrate_dict[name] = {'source_dir': '', 'link' : ''}
                        migrate_dict[name]['source_dir'] = os.path.join(path, name)
                        migrate_dict[name]['link'] = os.path.join(path, name).replace('\\', '/')[len(self.templates_path) + 1:]

        self.migrate_files(migrate_dict)
        self.parse_links(migrate_dict)

    def parse_links(self, migrate_dict):
        '''Iterates through every line in the html_content of an HTML document with the filename 'file_name' and
        adds /static/ to any line that should point to contents of the static folder of the flask app (i.e. lines that
        reference content of the css or javascript folder etc.).
        '''
        file_list = []
        templates_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                                      os.path.basename('Flaskerized_app'),
                                                      os.path.basename('templates'))
        js_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                                      os.path.basename('Flaskerized_app'),
                                                      os.path.basename('static'),
                                                      os.path.basename('js'))
        css_dir = os.path.join(os.path.dirname(flaskerizer.__file__),
                                                      os.path.basename('Flaskerized_app'),
                                                      os.path.basename('static'),
                                                      os.path.basename('css'))

        for html in os.listdir(templates_dir):
            file_list.append(os.path.join(templates_dir, os.path.basename(html)))
        for js in os.listdir(js_dir):
            file_list.append(os.path.join(js_dir, os.path.basename(js)))
        for css in os.listdir(css_dir):
            file_list.append(os.path.join(css_dir, os.path.basename(css)))
        for file in file_list:
            line_list = []
            with io.open(file, 'r') as read_obj:
                for line in read_obj:
                    line_list.append(line)
            os.remove(file)
            with io.open(file, 'a') as write_obj:
                for line in line_list:
                    for name in migrate_dict:
                        if migrate_dict[name]['link'] in line:
                            if name.endswith('.html'):
                                line = line.replace(migrate_dict[name]['link'], name)
                            elif name.endswith('.js'):
                                line = line.replace(migrate_dict[name]['link'], 'static/js/' + name)
                            elif name.endswith('.css'):
                                line = line.replace(migrate_dict[name]['link'], 'static/css/' + name)
                            elif name.endswith('.jpg'):
                                line = line.replace(migrate_dict[name]['link'], 'static/img/' + name)
                            elif name.endswith('.png'):
                                line = line.replace(migrate_dict[name]['link'], 'static/img/' + name)
                            elif name.endswith('.ico'):
                                line = line.replace(migrate_dict[name]['link'], 'static/img/' + name)
                            elif name.endswith('.otf'):
                                line = line.replace(migrate_dict[name]['link'], 'static/fonts/' + name)
                            elif name.endswith('.eot'):
                                line = line.replace(migrate_dict[name]['link'], 'static/fonts/' + name)
                            elif name.endswith('.svg'):
                                line = line.replace(migrate_dict[name]['link'], 'static/fonts/' + name)
                            elif name.endswith('.ttf'):
                                line = line.replace(migrate_dict[name]['link'], 'static/fonts/' + name)
                            elif name.endswith('.woff'):
                                line = line.replace(migrate_dict[name]['link'], 'static/fonts/' + name)
                            elif name.endswith('.woff2'):
                                line = line.replace(migrate_dict[name]['link'], 'static/fonts/' + name)
#'711.jpg': {'source_dir': 'C:\\Users\\vande060\\Desktop\\coding\\projects\\Flaskerizer\\Flaskerizer_src\\Examples\\Alstar_example\\img\\parallax\\1.jpg', 'link': 'img/parallax/1.jpg'}

                    write_obj.write(line)

if __name__ == "__main__":
    my_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'])
    my_object.make_folders()
    my_object.search_tree()




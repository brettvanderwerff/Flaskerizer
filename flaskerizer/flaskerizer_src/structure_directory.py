import io #needed to backport some open statements to python 2.7
import os
from flaskerizer.flaskerizer_src.target_folders import target_folders
from flaskerizer.flaskerizer_src.command_line_arguments import get_cmd_args
import multiprocessing
import numpy as np
import shutil
import time

class StructureDirectory():
    def __init__(self, templates_path, top_level_path, large_app_Structure):
        '''
        The top_level_path attribute of the StructureDirectory class is a path to the top level folder
         of the Bootstrap template source folder. The templates_path attribute of the StructureDirectory class is a
         path to the HTML files in the Bootstrap template source folder that will be migrated to the Flask 'templates'
        folder.
        '''
        self.top_level_path = top_level_path
        self.templates_path = templates_path
        self.base_app_dir = os.path.join(get_cmd_args()['app_path'], os.path.basename(get_cmd_args()['app_name']))
        if large_app_Structure == False:
            self.flaskerized_app_dir = self.base_app_dir
        elif large_app_Structure == True:
            self.flaskerized_app_dir = os.path.join(self.base_app_dir, os.path.basename(get_cmd_args()['app_name']))

    def mkdir(self):
        '''Makes all the folders for the Flask application.
        '''
        print('Making Flask app folders...')
        if os.path.exists(self.base_app_dir):
            shutil.rmtree(self.base_app_dir)
        os.mkdir(self.base_app_dir)
        if get_cmd_args()['large_app_structure'] == True:
            os.mkdir(self.flaskerized_app_dir)

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
                    shutil.rmtree(dir_path) #
                    os.makedirs(dir_path)


    def migrate_files(self, migrate_dict):
        '''Migration of all files detected by the detect_files method to their appropriate destinations in the
        Flaskerized_app directory (i.e. files with .css extension migrated to the css subfolder of the static folder.)
        '''
        print('Migrating static content to the static folder...')
        for name in migrate_dict:
            item_extension = name.split('.')[-1]
            shutil.copyfile(migrate_dict[name]['source_dir'],
                            os.path.join(self.flaskerized_app_dir,
                                         os.path.basename(target_folders[item_extension]['folder']),
                                         os.path.basename(target_folders[item_extension]['subfolder']),
                                         os.path.basename(name)))
            # ToDo fonts also need to be migrated to the css subfolder of static
    def detect_static_files(self):
        '''Walks through the entire directory tree of the Bootstrap template detecting any files with extensions that
        are needed for the static content of the Flask app (i.e. .css, .js, .img, etc). The names and locations of
        these files are saved in a dictionary.
        '''
        print('Finding static content...')
        migrate_dict = {}
        extensions = ['.js', '.css', '.jpg', '.png', 'gif', '.ico', '.otf', '.eot', '.svg', '.ttf', '.woff', '.woff2']
        path = self.top_level_path
        counter=0
        for path, subdir, files in os.walk(path):
            for name in files:
                counter +=1
                duplicate_name = str(counter).zfill(6) + name # this prevents issues 2+ files have same names
                for extension in extensions:
                    if name.endswith(extension):
                        migrate_dict[duplicate_name] = {'source_dir': '', 'link': ''}
                        migrate_dict[duplicate_name]['source_dir'] = os.path.join(path, name)
                        migrate_dict[duplicate_name]['link'] = os.path.join(path, name).replace('\\', '/')[
                                                     len(self.top_level_path) + 1:]

        return migrate_dict

    def detect_and_migrate_html_files(self):
        '''Detects files with the extension ".html" in the templates_path. These files are migrated to the "templates"
        folder of the Flaskerized_app directory.
        '''
        print('Finding and migrating HTML files to the templates folder...')
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


    def load_file(self, file):
        '''Iterates through each file in a file_list returned by the "file_list" method and loads them into memory as a
        list containing an item for each line of the file.
        '''
        line_list = []
        with io.open(file, 'r', encoding='utf-8') as read_obj:
            for line in read_obj:
                line_list.append(line)
        os.remove(file)
        return line_list
    
    def change_file_path(self,migrate_dict,name,file,line):
        '''For every line iterated by the parse_links method, the change_file_path method adds 
        the string "/static/" along with a string for the appropriate subfolder according to 
        the extension of file and changes link to new path.'''
        
        file_path = migrate_dict[name]['link']

        if ("../fonts/{}".format(name[6:])) in line:
            line = line.replace("../fonts/{}".format(name[6:]),"../fonts/{}".format(name))

        elif ("@import url('{}')".format(name[6:])) in line:
            line = line.replace("@import url('{}')".format(name[6:]),
                                "@import url('{}')".format(name))

        for extension in target_folders:
            if name.endswith(extension):

                full_path = (target_folders[extension]['folder'],
                            target_folders[extension]['subfolder'], name)
                            
                if ('../' + file_path) in line:
                    if file.endswith('.html'):
                        line = line.replace(file_path,'/'.join(full_path))
                    else:
                        line = line.replace(file_path,'/'.join(full_path[1:]))

                elif file_path in line:
                    line = line.replace(file_path,'/'.join(full_path))

                elif ('..' + file_path[file_path.find('/'):]) in line:
                    line = line.replace(file_path[file_path.find('/'):],
                                        '/'.join(('/' + str(full_path[1:]))))

                elif ('(../' + '/'.join(file_path.split('/')[2:])+ ')') in line:
                    line = line.replace('/'.join(file_path.split('/')[2:]),
                                        '/'.join(full_path[1:]))

        return line
    
    def parse_links(self, migrate_dict, file_list):
        '''Iterates through every file in the "file_list" argument and
        adds /static/ to any line that should point to contents of the static folder of the Flask app (i.e. lines that
        reference content of the css or javascript folder etc.).
        '''

        for file in file_list:
            line_list = self.load_file(file)

            with io.open(file, 'a', encoding='utf-8') as write_obj:

                for line in line_list:
                    for name in migrate_dict:
                        line = self.change_file_path(migrate_dict,name,file,line)

                    write_obj.write(line)

    def multi_proc(self, migrate_dict):
        '''
        Manages multi-processing of parse_links. Spawns a set of parse_links processes equal to the number of cores that
        the user has. Allows those processes to complete before moving on.
        '''
        print('Fixing links to reflect Flask app structure, this may take several minutes...')
        full_file_list = self.file_list() # complete list of all files that need to be parsed
        cores = multiprocessing.cpu_count()
        chunk_list = np.array_split(full_file_list, cores) # divide full_file_list by number of cores
        processess = [multiprocessing.Process(target=self.parse_links, args=(migrate_dict, sub_file_list)) for sub_file_list in chunk_list]
        for process in processess:
            process.start()
        for process in processess: # waits for set of spawned processes to complete before spawning more.
            process.join()

    def structure_directory(self):
        '''
        Structures the Flask project by making the 'templates' and 'static' folders and the appropriate subfolders.
        Migrates all static content (files with .css, .js, etc extensions) to the 'static' folder.
        Migrates all HTML files to the 'templates' folder. Parses all migrated files for links that need to be fixed to
        reflect the Flask project folder structure.
        '''
        self.mkdir()
        migrate_dict = self.detect_static_files()
        self.migrate_files(migrate_dict)
        self.detect_and_migrate_html_files()
        self.multi_proc(migrate_dict)








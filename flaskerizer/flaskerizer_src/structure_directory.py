import io #needed to backport some open statements to python 2.7
import os
from flaskerizer.flaskerizer_src.target_folders import target_folders
from flaskerizer.flaskerizer_src.command_line_arguments import get_cmd_args
import shutil

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
                duplicate_name = str(counter).zfill(6) + name
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

    def parse_links(self, migrate_dict):
        '''Iterates through every file returned by the "file_list" method and
        adds /static/ to any line that should point to contents of the static folder of the Flask app (i.e. lines that
        reference content of the css or javascript folder etc.).
        '''
        print('Fixing links to reflect Flask app structure, this may take several minutes...')

        file_list = self.file_list() 
        for file in file_list:
            line_list = self.load_file(file) 

            with io.open(file, 'a', encoding='utf-8') as write_obj:
                for line in line_list: 
                    for name in migrate_dict: 

                        full_address = (target_folders[extension]['folder'],
                                                        target_folders[extension]['subfolder'],
                                                         name)
                        address = migrate_dict[name]['link']  #file path without top_level_path        
                        query = address[address.find('/'):]   #file path after first "/"                  

                        if ("../fonts/{}".format(name[6:])) in line: 
                            line = line.replace("../fonts/{}".format(name[6:]),"../fonts/{}".format(name))

                        elif ("@import url('{}')".format(name[6:])) in line: 
                            line = line.replace("@import url('{}')".format(name[6:]),
                                                "@import url('{}')".format(name))

                        elif ('../' + address) in line: 
                            if file.endswith('.html'): 
                                if ('../' +address) in line:
                                    for extension in target_folders: 
                                        if name.endswith(extension):
                                            line = line.replace(address,'/'.join(full_address))
                            else:
                                for extension in target_folders: 
                                    if name.endswith(extension): 
                                        line = line.replace(address,'/'.join(full_address[1:]))
                                                           
                        elif address in line: 
                            for extension in target_folders:  
                                if name.endswith(extension): 
                                    line = line.replace(address,('/'.join(full_address)))

                        elif ('..' + query) in line:
                            for extension in target_folders:
                                if name.endswith(extension): 
                                    line = line.replace(query,'/'.join(('/' + full_address[1:])))
                                                       
                        elif ('(../' + '/'.join(address.split('/')[2:])+ ')') in line:
                            for extension in target_folders:
                                if name.endswith(extension):
                                    line = line.replace('/'.join(address.split('/')[2:]),'/'.join(full_address[1:]))
                                                       

                    write_obj.write(line) 

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
        self.parse_links(migrate_dict)








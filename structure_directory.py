import os
import shutil

class StructureDirectory():
    def __init__(self, directroy):
        self.directory = directroy

    def mkdir(self, dir):
        '''Makes folder of dir name in the working direectory.
        '''
        dir_path = os.path.join(os.getcwd(), os.path.basename(dir))
        if not os.path.exists(dir_path):
            print('generating {} folder'.format(dir))
            os.makedirs(dir_path)
        else:
            print('overwriting old {} folder'.format(dir))
            shutil.rmtree(os.path.join(os.getcwd(), os.path.basename(dir)))
            os.makedirs(dir_path)

    def migrate_static(self):
        '''Makes a static folder then migrates all the folders from the bootstrap template directory that belong in
        the static folder (css, js, etc) to the newly made static folder.
        '''
        self.mkdir('static')
        for item in os.listdir(self.directory):
            print('migrating {} to static folder'.format(item))
            item_path = os.path.join(self.directory, os.path.basename(item))
            if os.path.isdir(item_path):
                shutil.copytree(item_path,
                                os.path.join(os.getcwd(), os.path.basename('static'), os.path.basename(item)))

    def migrate_templates(self, html_content, file_name):
        '''Iterates through every line in the html_content of an HTML document with the filename 'file_name' and
        adds /static/ to any line that should point to contents of the static folder of the flask app (i.e. lines that
        reference content of the css or js folder etc.).
        '''
        write_directory = os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename(file_name))
        for line in html_content:
            with open(write_directory, 'a') as write_obj:
                for folder in os.listdir(os.path.join(os.getcwd(), os.path.basename('static'))):
                    if ('=\"' + str(folder) + "/") in line:
                        split_line = line.split("\"" + str(folder) + "/")
                        line = ("\"" + '/static/' + (str(folder) + "/")).join(split_line)
                write_obj.write(line)

    def parse_html(self):
        '''Locates all the HTML files in the Bootstrap template directory.
        '''
        self.mkdir('templates')
        for file_name in os.listdir(self.directory):
            if '.html' in file_name:
                print('generating content for {} and migrating content to templates folder'.format(file_name))
                source_directory = os.path.join(self.directory, os.path.basename(file_name))
                with open(source_directory) as html_content:
                    self.migrate_templates(html_content, file_name) # <link href="css/style.css" rel="stylesheet"> makes an error

if __name__ == "__main__":
    my_object = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))
    my_object.migrate_static()
    my_object.parse_html()



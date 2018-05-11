import os
import shutil

class Flaskerizer():
    def __init__(self, directroy):
        self.directory = directroy

    def mkdir(self, dir):
        '''Makes folder of dir name in base '''
        dir_path = os.path.join(os.getcwd(), os.path.basename(dir))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def migrate_static(self):
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('static')))
        self.mkdir('static')
        for item in os.listdir(self.directory):
            item_path = os.path.join(self.directory, os.path.basename(item))
            if os.path.isdir(item_path):
                shutil.copytree(item_path,
                                os.path.join(os.getcwd(), os.path.basename('static'), os.path.basename(item)))

    def migrate_templates(self, html_content, file_name):
        write_directory = os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename(file_name))
        for line in html_content:
            with open(write_directory, 'a') as write_obj:
                for folder in os.listdir(os.path.join(os.getcwd(), os.path.basename('static'))):
                    if ('=\"' + str(folder) + "/") in line:
                        split_line = line.split("\"" + str(folder) + "/")
                        line = ("\"" + '/static/' + (str(folder) + "/")).join(split_line)
                write_obj.write(line)

    def parse_html(self):
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('templates')))
        self.mkdir('templates')
        for file_name in os.listdir(self.directory):
            if '.html' in file_name:
                source_directory = os.path.join(self.directory, os.path.basename(file_name))
                with open(source_directory) as html_content:
                    self.migrate_templates(html_content, file_name)

if __name__ == "__main__":
    my_object = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
    my_object.migrate_static()
    my_object.parse_html()



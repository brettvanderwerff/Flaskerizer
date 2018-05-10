import os
import shutil

class Flaskerizer():
    def __init__(self, directroy):
        self.directory = directroy

    def mkdir(self, dir):
        dir_path = os.path.join(os.getcwd(), os.path.basename(dir))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def migrate_static(self):
        self.mkdir('static')
        for item in os.listdir(self.directory):
            item_path = os.path.join(self.directory, os.path.basename(item))
            if os.path.isdir(item_path):
                shutil.copytree(item_path,
                                os.path.join(os.getcwd(), os.path.basename('static'), os.path.basename(item)))

    def migrate_templates(self):
        self.mkdir('templates')
        for item in os.listdir(self.directory):
            print(item)
            item_path = os.path.join(self.directory, os.path.basename(item))
            if os.path.isfile(item_path):
                shutil.copyfile(item_path, #ToDo only copy files that have .html extension by using ReGex
                                os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename(item)))

    def parse_templates(self):
        for item in os.listdir(os.path.join(os.getcwd(), os.path.basename('templates'))):
            with open(os.path.join(os.getcwd(), os.path.basename('templates'), os.path.basename(item))) as read_obj:
                for line in read_obj:
                    for folder in os.listdir(os.path.join(os.getcwd(), os.path.basename('static'))):
                        if ('=\"' + str(folder) + "/") in line: #https://stackoverflow.com/questions/1325905/inserting-line-at-specified-position-of-a-text-file
                            print(line)                         #This needs to be more selective
                            split_line = line.split("\"" + str(folder) + "/")
                            join_line = ("\"" + '/static/' + (str(folder) + "/")).join(split_line)
                            print(join_line)



if __name__ == "__main__":
    my_object = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
    my_object.parse_templates()



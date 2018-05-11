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
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('static')))
        self.mkdir('static')
        for item in os.listdir(self.directory):
            item_path = os.path.join(self.directory, os.path.basename(item))
            if os.path.isdir(item_path):
                shutil.copytree(item_path,
                                os.path.join(os.getcwd(), os.path.basename('static'), os.path.basename(item)))

    def write_templates(self):
        #This needs to be refactored for readability
        shutil.rmtree(os.path.join(os.getcwd(), os.path.basename('templates')))
        self.mkdir('templates')
        for item in os.listdir(self.directory):
            if '.html' in item:
                with open(os.path.join(self.directory, os.path.basename(item))) as read_obj:
                    for line in read_obj:
                        with open(os.path.join(os.getcwd(), os.path.basename('templates'),
                                               os.path.basename(item)), 'a') as write_obj:
                            for folder in os.listdir(os.path.join(os.getcwd(), os.path.basename('static'))):
                                if ('=\"' + str(folder) + "/") in line:
                                    split_line = line.split("\"" + str(folder) + "/")
                                    line = ("\"" + '/static/' + (str(folder) + "/")).join(split_line)
                            write_obj.write(line)

if __name__ == "__main__":
    my_object = Flaskerizer(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Folio')
    my_object.migrate_static()
    my_object.write_templates()



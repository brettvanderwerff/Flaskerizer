import flaskerizer
from Flaskerizer_src.config import CONFIGURATION
from Flaskerizer_src.HTTP_status_dict import HTTP_status_dict
from Flaskerizer_src.status_code_to_word import status_code_to_word
import os

class WriteApp():
    def __init__(self):
        self.base_app_dir = os.path.join(os.path.dirname(flaskerizer.__file__), os.path.basename('Flaskerized_app'))
        if CONFIGURATION['large_app_structure'] == False:
            self.flaskerized_app_dir = self.base_app_dir
        elif CONFIGURATION['large_app_structure'] == True:
            self.flaskerized_app_dir = os.path.join(self.base_app_dir, os.path.basename('Flaskerized_app'))

    def get_routes(self):
        '''Gets the name of every HTML template in the templates folder.
        '''
        return [template for template in os.listdir(os.path.join(self.flaskerized_app_dir,
                                                                 os.path.basename('templates')))]

    def write_error_handler(self, template_name, write_obj):
        '''If the write_routes function detects a template name as containing a status code, the template name will
        be passed to write_error_handler along with the write_obj. The write_error_handler function will write an
        error handler for the template, which is making the assumption that the template was intended to represent
        an error code.
        '''
        status_code = template_name.strip('.html')
        function_name = status_code_to_word(status_code)
        write_obj.write('@app.errorhandler({})\n'.format(status_code))
        write_obj.write('def {}(e):\n'.format(function_name))
        write_obj.write("    return render_template('{}'), {}\n\n".format(template_name, status_code))

    def write_routes(self, write_obj):
        '''For every HTML template in the 'templates' folder, write_routes generates a function that is bound to the
        URL for that template by the route() decorator. See http://flask.pocoo.org/docs/1.0/quickstart/#routing
        for more info.
        '''
        for template_name in self.get_routes():
            if template_name.strip('.html') in HTTP_status_dict.keys():
                self.write_error_handler(template_name, write_obj)
                continue
            write_obj.write("@app.route('/{}')\n".format(template_name))
            if template_name == "index.html":
                write_obj.write("@app.route('/')\n")
            write_obj.write('def {}():\n'.format(template_name.strip('.html').replace('-','_')))
            write_obj.write("    return render_template('{}')\n\n".format(template_name))


    def write_setup(self):
        with open(os.path.join(self.base_app_dir, os.path.basename('setup.py')), 'w') as write_obj:
            write_obj.write('from setuptools import setup\n\n'
                            'setup(\n'
                            '   name=\'Flaskerized_app\',\n'
                            '   packages=[\'Flaskerized_app\'],\n'
                            '   include_package_data=True,\n'
                            '   install_requires=[\n'
                            '       \'flask\',\n'
                            '   ],\n'
                            ')')

    def write_small_app(self):
        '''Writes the 'skeleton' of a Flask app in a file 'app.py'. Writes import statements for Flask and
        render_template, instantiates an object 'app' from the 'Flask' class, and generates a conditional
        'if __name__ == '__main__':' to run the Flask app.
         URL routes are added to the 'skeleton' by calling the write_routes method.
         '''
        with open(os.path.join(self.flaskerized_app_dir, os.path.basename('app.py')), 'w') as write_obj:
            write_obj.write('from flask import Flask, render_template\n\n')
            write_obj.write('app = Flask(__name__)\n\n')
            self.write_routes(write_obj)
            write_obj.write("if __name__ == '__main__':\n")
            write_obj.write("    app.run()")

    def write_large_app(self):
        with open(os.path.join(self.flaskerized_app_dir, os.path.basename('__init__.py')), 'w') as write_obj:
            write_obj.write('from flask import Flask\n'
                            'app = Flask(__name__)\n\n'
                            'import Flaskerized_app.routes')
        with open(os.path.join(self.flaskerized_app_dir, os.path.basename('routes.py')), 'w') as write_obj:
            write_obj.write('from flask import render_template\n'
                            'from Flaskerized_app import app\n\n')
            self.write_routes(write_obj)
        self.write_setup()


if __name__ == '__main__':
    my_object = WriteApp()
    my_object.write_small_app()






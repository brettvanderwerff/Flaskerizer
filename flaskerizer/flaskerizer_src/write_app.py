from flaskerizer.flaskerizer_src.HTTP_status_dict import HTTP_status_dict
from flaskerizer.flaskerizer_src.status_code_to_word import status_code_to_word
from flaskerizer.flaskerizer_src.command_line_arguments import get_cmd_args
import os

class WriteApp():
    def __init__(self):
        self.base_app_dir = os.path.join(get_cmd_args()['app_path'], os.path.basename(get_cmd_args()['app_name']))
        if get_cmd_args()['large_app_structure'] == False:
            self.flaskerized_app_dir = self.base_app_dir
        elif get_cmd_args()['large_app_structure'] == True:
            self.flaskerized_app_dir = os.path.join(self.base_app_dir, os.path.basename(get_cmd_args()['app_name']))

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
        print('Writing routes...')
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
        '''
        Writes a setup.py file for the large Flask app project structure.
        '''
        print('Writing setup.py...')
        with open(os.path.join(self.base_app_dir, os.path.basename('setup.py')), 'w') as write_obj:
            write_obj.write('from setuptools import setup\n\n'
                            'setup(\n'
                            '   name=\'{}\',\n'
                            '   packages=[\'{}\'],\n'
                            '   include_package_data=True,\n'
                            '   install_requires=[\n'
                            '       \'flask\',\n'
                            '   ],\n'
                            ')'.format(get_cmd_args()['app_name'], get_cmd_args()['app_name']))


    def write_small_app(self):
        '''
        Writes an instantiation of a Flask app in a Python module according to the small Flask app project structure.
        Also writes the routes in the same file.
        '''
        print('Writing Flask app module...')
        with open(os.path.join(self.flaskerized_app_dir,
                               os.path.basename('{}.py'.format(get_cmd_args()['app_name']))),'w') as write_obj:
            write_obj.write('from flask import Flask, render_template\n\n')
            write_obj.write('app = Flask(__name__)\n\n')
            self.write_routes(write_obj)
            write_obj.write("if __name__ == '__main__':\n")
            write_obj.write("    app.run()")
        print('Flaskerization complete')

    def write_large_app(self):
        '''
        Writes an instantiation of a Flask app in an '__init__.py' file according to the large Flask app project
        structure detailed in the Flask documentation:
        http://flask.pocoo.org/docs/1.0/patterns/packages/
        Writes the routes in a separate routes.py file.
        '''
        print('Writing Flask app package...')
        with open(os.path.join(self.flaskerized_app_dir, os.path.basename('__init__.py')), 'w') as write_obj:
            write_obj.write('from flask import Flask\n'
                            'app = Flask(__name__)\n\n'
                            'import {}.routes'.format(get_cmd_args()['app_name']))
        with open(os.path.join(self.flaskerized_app_dir, os.path.basename('routes.py')), 'w') as write_obj:
            write_obj.write('from flask import render_template\n'
                            'from {} import app\n\n'.format(get_cmd_args()['app_name']))
            self.write_routes(write_obj)
        self.write_setup()
        print('Flaskerization complete')









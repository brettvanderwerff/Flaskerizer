import os
from HTTP_status_dict import HTTP_status_dict
from status_code_to_word import status_code_to_word

class WriteApp():

    def get_routes(self):
        return [template for template in os.listdir(os.path.join(os.getcwd(), os.path.basename('templates')))]

    def write_error_handler(self, template_name, write_obj): #ToDo eliminate non-error status codes from dictionary
        status_code = template_name.strip('.html')
        function_name = status_code_to_word(status_code)
        write_obj.write('@app.errorhandler({})\n'.format(status_code))
        write_obj.write('def {}(e):\n'.format(function_name))
        write_obj.write("    return render_template('{}'), {}\n\n".format(template_name, status_code))

    def write_routes(self, write_obj):
        for template_name in self.get_routes():
            if template_name.strip('.html') in HTTP_status_dict.keys():
                self.write_error_handler(template_name, write_obj)
                continue
            write_obj.write("@app.route('/{}')\n".format(template_name))
            write_obj.write('def {}():\n'.format(template_name.strip('.html').replace('-','_')))
            write_obj.write("    return render_template('{}')\n\n".format(template_name))

    def write_app(self):
        with open('app.py', 'w') as write_obj:
            write_obj.write('from flask import Flask, render_template\n\n')
            write_obj.write('app = Flask(__name__)\n\n')
            self.write_routes(write_obj)
            write_obj.write("if __name__ == '__main__':\n")
            write_obj.write("    app.run()")




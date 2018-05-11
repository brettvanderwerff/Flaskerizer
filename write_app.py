import os

class WriteApp():

    def get_routes(self):
        return [template for template in os.listdir(os.path.join(os.getcwd(), os.path.basename('templates')))]

    def write_routes(self, write_obj):
        for template in self.get_routes():
            write_obj.write("@app.route('/{}')\n".format(template))
            write_obj.write('def {}():\n'.format(template.strip('.html').replace('-','_')))
            write_obj.write("    return render_template('{}')\n\n".format(template))


    def write_app(self):
        with open('app.py', 'w') as write_obj:
            write_obj.write('from flask import Flask, render_template\n\n')
            write_obj.write('app = Flask(__name__)\n\n')
            self.write_routes(write_obj)
            write_obj.write("if __name__ == '__main__':\n")
            write_obj.write("    app.run()")



my_object = WriteApp()
my_object.write_app()
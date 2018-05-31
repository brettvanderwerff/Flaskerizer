from structure_directory import StructureDirectory
from write_app import WriteApp
try:
    from Tkinter import Tk
    import tkFileDialog as filedialog
except:
    import tkinter as Tk
    from tkinter import filedialog
"""The gui for flaskerizer is a simple graphical interface for the Flaskerizer program

It does the same but instead of putting the folder path on the config.py file you select inside the GUI
"""

class ChooseFilesGUI(object):
    """This Class cointains everything related to the Graphical interface
    
    It contains some functions for the buttons and for organization
    """
    def __init__(self, is_test=False):
        self.root = Tk.Tk()
        self.root.title = "Flaskerizer"
        self.html_location = Tk.StringVar()
        self.static_location = Tk.StringVar()
        self.js_location = Tk.StringVar()
        self.html_location.set("The folder with .html files")
        self.static_location.set("The folder with images, .css, etc")
        self.js_location.set("The folder with the .js files")
        self.main_layout()
        self.is_test = is_test
        if not self.is_test:
            self.root.mainloop()
        else:
            pass
 
    def main_layout(self):
        """Outputs buttons, Labels and entries to the window
        """
        self.main = Tk.Frame(self.root)
        self.label_html = Tk.Label(self.main,
                        text = "Html Files Location:")
        self.label_html.grid(row = 0, column=0, sticky="WENS", pady=20)

        self.folder_search_html = Tk.Button(self.main,
                        text = "Search Files", command=self.get_html_folder)
        self.folder_search_html.grid(row=0, column=1,sticky="WENS", pady=20)
        
        self.folder_location_html = Tk.Entry(self.main,
                        textvariable = self.html_location, width = 50)
        self.folder_location_html.grid(row=0,column=2,sticky="WENS", pady = 20)
        
        self.label_static = Tk.Label(self.main,
                        text = "Static Files Location:")
        self.label_static.grid(row = 1, column = 0, sticky="WENS", pady=20)
        
        self.folder_search_static = Tk.Button(self.main,
                        text = "Search Files", command=self.get_static_folder)
        self.folder_search_static.grid(row=1,column=1,sticky="WENS",pady = 20)
        
        self.folder_location_static = Tk.Entry(self.main,
                        textvariable = self.static_location, width = 50)
        self.folder_location_static.grid(row=1,column=2,sticky="WENS",pady=20)
        
        self.label_js = Tk.Label(self.main,
                        text = "Java Script Files Location:")
        self.label_js.grid(row = 2, column = 0, sticky="WENS", pady = 20)
        
        self.folder_search_js = Tk.Button(self.main,
                        text = "Search Files", command=self.get_js_folder)
        self.folder_search_js.grid(row=2, column=1, sticky="WENS", pady=20)
        
        self.folder_location_js = Tk.Entry(self.main,
                        textvariable = self.js_location, width = 50)
        self.folder_location_js.grid(row=2, column=2, sticky="WENS", pady = 20)
        
        self.main.pack()
        self.ok_button = Tk.Button(self.root,
                                    text = "OK", command=self.get_values).pack()
    def get_html_folder(self):
        """Opens A file dialog for selecting the html folder
        """
        path = filedialog.askdirectory()
        self.html_location.set(path)

    def get_static_folder(self):
        """Opens A file dialog for selecting the static folder
        """
        path = filedialog.askdirectory()
        self.static_location.set(path)

    def get_js_folder(self):
        """Opens A file dialog for selecting the js folder
        """
        path = filedialog.askdirectory()
        self.js_location.set(path)

    def get_values(self):
        """Gets the path on the html, static and js entries
        quits the window and return the values
        """
        html = self.html_location.get()
        static, js = self.static_location.get(), self.js_location.get()
        self.root.quit()
        return [html, static, js]



if __name__ == '__main__':
    values_from_gui = ChooseFilesGUI().get_values()
    structure_directory_object = StructureDirectory(templates_path=values_from_gui[0],
                                                static_path=values_from_gui[1],
                                                javascript_path=values_from_gui[2])
    write_app_object = WriteApp()
    structure_directory_object.migrate_static()
    structure_directory_object.parse_html()
    structure_directory_object.parse_javascript()
    write_app_object.write_app()

from structure_directory import StructureDirectory
from write_app import WriteApp
import os
try:
    import Tkinter as tk
    import tkFileDialog as filedialog
except:
    import tkinter as tk
    from tkinter import filedialog

"""The gui for flaskerizer is a simple graphical interface for the Flaskerizer program

It does the same but instead of putting the folder path on the config.py file you select inside the GUI
"""


class ChooseFilesGUI(object):
    """This Class cointains everything related to the Graphical interface

    It contains some functions for the buttons and for organization
    """

    def __init__(self, is_test=False):
        self.root = tk.Tk()
        self.root.title("Flaskerizer")
        self.html_location = tk.StringVar()
        self.static_location = tk.StringVar()
        self.js_location = tk.StringVar()
        self.html_location.set(
            "Select the main html file, usually a index.html file")
        self.static_location.set(
            "The folder with images, .css, etc. If separated select the main folder")
        self.js_location.set(
            "Select the a .js file, one in the js folder if there is one")
        self.main_layout()
        self.is_test = is_test
        if not self.is_test:
            self.root.mainloop()
        else:
            pass

    def main_layout(self):
        """Outputs buttons, Labels and entries to the window
        """
        self.main = tk.Frame(self.root)
        self.label_html = tk.Label(self.main,
                                   text="Html Files Location:")
        self.label_html.grid(row=0, column=0, sticky="WENS", pady=20)

        self.folder_search_html = tk.Button(self.main,
                                            text="Search Files", command=self.get_html_folder)
        self.folder_search_html.grid(row=0, column=1, sticky="WENS", pady=20)

        self.folder_location_html = tk.Entry(self.main,
                                             textvariable=self.html_location, width=80)
        self.folder_location_html.grid(row=0, column=2, sticky="WENS", pady=20)

        self.label_static = tk.Label(self.main,
                                     text="Static Files Location:")
        self.label_static.grid(row=1, column=0, sticky="WENS", pady=20)

        self.folder_search_static = tk.Button(self.main,
                                              text="Search Files", command=self.get_static_folder)
        self.folder_search_static.grid(row=1, column=1, sticky="WENS", pady=20)

        self.folder_location_static = tk.Entry(self.main,
                                               textvariable=self.static_location, width=80)
        self.folder_location_static.grid(
            row=1, column=2, sticky="WENS", pady=20)

        self.label_js = tk.Label(self.main,
                                 text="Java Script Files Location:")
        self.label_js.grid(row=2, column=0, sticky="WENS", pady=20)

        self.folder_search_js = tk.Button(self.main,
                                          text="Search Files", command=self.get_js_folder)
        self.folder_search_js.grid(row=2, column=1, sticky="WENS", pady=20)

        self.folder_location_js = tk.Entry(self.main,
                                           textvariable=self.js_location, width=80)
        self.folder_location_js.grid(row=2, column=2, sticky="WENS", pady=20)

        self.main.pack()
        self.ok_button = tk.Button(self.root,
                                   text="OK", command=self.get_values).pack()

    def get_html_folder(self):
        """Opens A file dialog for selecting the main html file
        """
        path = filedialog.askopenfilename(title= "Select the man html file normally index.html",
        filetypes=(("Html Files", "*.html"), ("all files", "*.*")))
        path = self.path_to_folder(path)
        self.html_location.set(path)

    def get_static_folder(self):
        """Opens A file dialog for selecting the static folder
        """
        path = filedialog.askdirectory(title="Select the main static folder")
        self.static_location.set(path)

    def get_js_folder(self):
        """Opens A file dialog for selecting a js file
        """
        path = filedialog.askopenfilename(title = "Select a .js file, normally inside the js folder",
        filetypes=(("Javascript Files", "*.js"), ("all files", "*.*")))
        path = self.path_to_folder(path)
        self.js_location.set(path)

    def path_to_folder(self, path):
        """Transforms a File path into a folder path
        """
        return os.path.split(path)[0]

    def get_values(self):
        """Gets the path on the html, static and js entries
        uses the flaskerizer
        """
        self.html = self.html_location.get()
        self.static, self.js = self.static_location.get(), self.js_location.get()
        if not self.is_test:
            self.structure_directory_object = StructureDirectory(templates_path=self.html,
                                                            static_path=self.static,
                                                            javascript_path=self.js)
            self.write_app_object = WriteApp()
            self.structure_directory_object.migrate_static()
            self.structure_directory_object.parse_html()
            self.structure_directory_object.parse_javascript()
            self.write_app_object.write_app()
            self.root.quit()
        return [self.html, self.static, self.js]


if __name__ == '__main__':
    ChooseFilesGUI()

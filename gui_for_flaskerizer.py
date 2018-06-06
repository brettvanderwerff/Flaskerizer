from structure_directory import StructureDirectory
from write_app import WriteApp
import os
try:
    import Tkinter as tk
    import tkFileDialog as filedialog
except ImportError:
    import tkinter as tk
    from tkinter import filedialog

"""The GUI for Flaskerizer is a simple graphical interface for the Flaskerizer program

Instead of putting path values in the config.py file
it generates a popup Graphical User Interface (GUI) window
prompting the user to select the paths from the bootstrap theme
that he wants to flaskerize.
"""


class ChooseFilesGUI(object):
    """The ChooseFilesGUI class generates a popup graphical user interface (GUI)
    prompting the user to select paths pointing to folder content from the
    Bootstrap template that will be migrated to the 'templates',
    'static', and javascript folders of the Flask app.
    This GUI functions as an alternative to requiring the user
    to manually enter these paths in the config.py file.
    """

    def __init__(self, is_test=False):
        self.root = tk.Tk()
        self.root.title("Flaskerizer")
        self.html_location = tk.StringVar()
        self.static_location = tk.StringVar()
        self.js_location = tk.StringVar()
        self.html_location.set(
            "Select the main HTML file, usually a index.html file")
        self.static_location.set(
            "Select the folder that contains the css and img folders or the one with CSS and images files")
        self.js_location.set(
            "Select one JavaScript (.js) file from the template JavaScript folder")
        self.main_layout()
        self.is_test = is_test
        if not self.is_test:        #For testing purposes, make it unable to open the window.
            self.root.mainloop()
        else:
            pass

    def main_layout(self):
        """The program layout, it outputs all the buttons,
        Labels and Entries seen on the window.
        """

        self.main = tk.Frame(self.root)
        self.label_html = tk.Label(self.main,
                                   text="HTML Files Location:")
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
        self.folder_location_static.grid(row=1, column=2, sticky="WENS", pady=20)


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
        """Opens a file dialog prompting the user to select the main HTML file.
        Gets the directory path with the path_to_folder function
        and sets the html_location variable with the returned path value.
        """

        path = filedialog.askopenfilename(title= "Select the man html file normally index.html",
        filetypes=(("Html Files", "*.html"), ("all files", "*.*")))
        path = self.path_to_folder(path)
        self.html_location.set(path)

    def get_static_folder(self):
        """Opens a file dialog prompting the user to select the static folder.
        Gets the path, and sets the static_location to the path value.
        """

        path = filedialog.askdirectory(title="Select the main static folder")
        self.static_location.set(path)

    def get_js_folder(self):
        """Opens a file dialog prompting the user to select the JavaScript file.
        Gets the directory path with the path_to_folder function
        and sets the js_location variable with the returned path value.
        """

        path = filedialog.askopenfilename(title = "Select a .js file, normally inside the js folder",
        filetypes=(("Javascript Files", "*.js"), ("all files", "*.*")))
        path = self.path_to_folder(path)
        self.js_location.set(path)

    def path_to_folder(self, path):
        """Transforms a File path into a folder path
        stripping the file name from the path,
        leaving only the directory path.
        """

        return os.path.split(path)[0]

    def get_values(self):
        """Gets the html_location, static_location and js_location
        values and sets them to new variables then uses them
        for running flaskerizer.
        """
        self.html = self.html_location.get()
        self.static, self.js = self.static_location.get(), self.js_location.get()
        if not self.is_test:        #For testing purposes making the program unable to make new folders.
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

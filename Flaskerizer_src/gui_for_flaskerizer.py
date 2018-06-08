from Flaskerizer_src.structure_directory import StructureDirectory
from Flaskerizer_src.write_app import WriteApp

import os
try:
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

except ImportError:
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox


class ChooseFilesGUI(object):
    """The ChooseFilesGUI class generates a Pop-up graphical user interface (GUI)
    prompting the user to select paths pointing to folder content from the
    Bootstrap template that will be migrated to the 'templates',
    'static', and JavaScript folders of the Flask APP.
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
            "Select one HTML file from the template")
        self.static_location.set(
            "Select the template folder containing all the css, img, js folders")
        self.js_location.set(
            "Select one JavaScript (.js) file from the template JavaScript folder")
        self.main_layout()
        self.is_test = is_test
        if not self.is_test:        #For testing purposes, make it unable to open the window.
            self.root.mainloop()
        else:
            pass

    def main_layout(self):
        """The GUI layout, defines all the buttons,
        labels, and entries seen on the window.
        """

        self.main = tk.Frame(self.root)
        self.label_html = tk.Label(self.main,
                                   text="HTML File Location:")
        self.label_html.grid(row=0, column=0, sticky="WENS", pady=20)
        self.folder_search_html = tk.Button(self.main,
                                            text="Search Files", command=self.get_html_folder)
        self.folder_search_html.grid(row=0, column=1, sticky="WENS", pady=20)
        self.folder_location_html = tk.Entry(self.main,
                                             textvariable=self.html_location, width=80)
        self.folder_location_html.grid(row=0, column=2, sticky="WENS", pady=20)


        self.label_static = tk.Label(self.main,
                                     text="Static Folder Location:")
        self.label_static.grid(row=1, column=0, sticky="WENS", pady=20)
        self.folder_search_static = tk.Button(self.main,
                                              text="Search Files", command=self.get_static_folder)
        self.folder_search_static.grid(row=1, column=1, sticky="WENS", pady=20)
        self.folder_location_static = tk.Entry(self.main,
                                               textvariable=self.static_location, width=80)
        self.folder_location_static.grid(row=1, column=2, sticky="WENS", pady=20)


        self.label_js = tk.Label(self.main,
                                 text="JavaScript File Location:")
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
        """Opens a file dialog prompting the user to select an HTML file.
        Gets the directory path with the path_to_folder function
        and sets the html_location variable with the returned path value.
        """

        path = filedialog.askopenfilename(title= "Select the main html file normally index.html",
        filetypes=(("Html Files", "*.html"), ("all files", "*.*")))
        self.html_location.set(path)
        if self.validate_path(path):
            self.html_location.set(path)
        else:
            self.html_location.set("Please select a valid html file")

    def get_static_folder(self):
        """Opens a file dialog prompting the user to select the static folder.
        Gets the path, and sets the static_location to the path value.
        """

        path = filedialog.askdirectory(title="Select the main static folder")
        if self.validate_path(path):
            self.static_location.set(path)
        else:
            self.static_location.set("Please select a valid static folder")

    def get_js_folder(self):
        """Opens a file dialog prompting the user to select a JavaScript file.
        Gets the directory path with the path_to_folder function
        and sets the js_location variable with the returned path value.
        """

        path = filedialog.askopenfilename(title = "Select a .js file, normally inside the js folder",
        filetypes=(("JavaScript Files", "*.js"), ("all files", "*.*")))
        if self.validate_path(path):
            self.js_location.set(path)
        else:
            self.js_location.set("Please select a valid js file")

    def path_to_folder(self, path):
        """Transforms a File path into a folder path
        stripping the file name from the path,
        leaving only the directory path.
        """

        return os.path.split(path)[0]
    def validate_path(self, path):
        """Validates the path making sure it exists
        """
        if os.path.exists(path):
            return True
        else:
            return False

    def validate_entries(self):
        """Validates all entries and if
        there is errors a error pop-up window appears
        """
        self.error_entries = []
        html = self.validate_path(self.html_location.get())
        static = self.validate_path(self.static_location.get())
        js = self.validate_path(self.js_location.get())
        if not html:
            self.error_entries.append("'Html File location' ")
        if not static:
            self.error_entries.append("'Static Files location' ")
        if not js:
            self.error_entries.append("'JavaScript File location' ")
        if not html or not static or not js:
            self.error_message = "There is errors in the entries: "
            for x in self.error_entries:
                self.error_message = self.error_message + x 
            messagebox.showerror("Entries Error", self.error_message)
            return False
        else:
            return True

    def get_values(self):
        """Gets the html_location, static_location and js_location
        values and sets them to new variables then uses them
        for running Flaskerizer.
        """
        if self.validate_entries():
            self.html = self.path_to_folder(self.html_location.get())
            self.static = self.static_location.get()
            self.js = self.path_to_folder(self.js_location.get())
            if not self.is_test:        #For testing purposes making the program unable to make new folders.
                self.root.quit()
                self.structure_directory_object = StructureDirectory(templates_path=self.html,
                                                                static_path=self.static,
                                                                javascript_path=self.js)
                self.write_app_object = WriteApp()
                self.structure_directory_object.migrate_static()
                self.structure_directory_object.parse_html()
                self.structure_directory_object.parse_javascript()
                self.write_app_object.write_app()
            return [self.html, self.static, self.js]        #For testing purposes returns values


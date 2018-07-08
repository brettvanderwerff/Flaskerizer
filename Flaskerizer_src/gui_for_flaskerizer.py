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
        self.templates_path = tk.StringVar()
        self.top_level_path = tk.StringVar()
        self.top_level_path.set(
            "Select the 'top level' folder of the Bootstrap template")
        self.templates_path.set(
            "Select one HTML file from the main HTML folder of the Bootstrap template")
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

        self.label_static = tk.Label(self.main,
                                     text="Top Level Path Location:")
        self.label_static.grid(row=0, column=0, sticky="WENS", pady=20)
        self.folder_search_static = tk.Button(self.main,
                                              text="Search Files", command=self.get_static_folder)
        self.folder_search_static.grid(row=0, column=1, sticky="WENS", pady=20)
        self.folder_location_static = tk.Entry(self.main,
                                               textvariable=self.top_level_path, width=80)
        self.folder_location_static.grid(row=0, column=2, sticky="WENS", pady=20)

        self.label_html = tk.Label(self.main,
                                   text="Templates Path Location:")
        self.label_html.grid(row=1, column=0, sticky="WENS", pady=20)
        self.folder_search_html = tk.Button(self.main,
                                            text="Search Files", command=self.get_templates_path)
        self.folder_search_html.grid(row=1, column=1, sticky="WENS", pady=20)
        self.folder_location_html = tk.Entry(self.main,
                                             textvariable=self.templates_path, width=80)
        self.folder_location_html.grid(row=1, column=2, sticky="WENS", pady=20)

        self.main.pack()
        self.ok_button = tk.Button(self.root,
                                   text="OK", command=self.get_values).pack()

    def get_templates_path(self):
        """Opens a file dialog prompting the user to select an HTML file.
        Gets the directory path with the path_to_folder function
        and sets the html_location variable with the returned path value.
        """

        path = filedialog.askopenfilename(title= "Select one HTML file from the main HTML folder of the Bootstrap template",
        filetypes=(("Html Files", "*.html"), ("all files", "*.*")))
        if self.validate_path(path) and path.endswith(".html"):
            self.templates_path.set(path)
        elif path == "":
            self.templates_path.set("Select one HTML file from the main HTML folder of the Bootstrap template")
        elif not path.endswith(".html"):
            messagebox.showinfo("Info", "Please select an HTML (.html) file type.")

    def get_static_folder(self):
        """Opens a file dialog prompting the user to select the static folder.
        Gets the path, and sets the static_location to the path value.
        """

        path = filedialog.askdirectory(title="Select the 'top level' folder of the Bootstrap template")
        if self.validate_path(path):
            self.top_level_path.set(path)
        else:
            self.top_level_path.set("Select the 'top level' folder of the Bootstrap template")



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
        there are errors an error pop-up window appears
        """

        self.error_entries = []
        html = self.validate_path(self.templates_path.get())
        static = self.validate_path(self.top_level_path.get())
        if not html:
            self.error_entries.append("'Html File location' ")
            self.error_message = "There are errors in the following entries: "
            for x in self.error_entries:
                self.error_message = self.error_message + x
            messagebox.showerror("Entries Error", self.error_message)
            return False
        if not static:
            self.error_entries.append("'Top level folder location' ")
        else:
            return True

    def get_values(self):
        """Gets the templates_path and top_level_path values of Bootstrap template.
        These paths are passed to the StructureDirectory class for flaskerization.
        """
        self.templates = self.templates_path.get()
        self.top_level = self.top_level_path.get()
        if not self.is_test:        #For testing purposes making the program unable to make new folders or windows.
            if self.validate_entries():
                self.templates = self.path_to_folder(self.templates)
                self.root.quit()
                self.structure_directory_object = StructureDirectory(templates_path=self.templates,
                                                                     top_level_path=self.top_level)
                self.write_app_object = WriteApp()
                self.structure_directory_object.structure_directory()
                self.write_app_object.write_app()
        return [self.templates, self.top_level]        #For testing purposes returns values


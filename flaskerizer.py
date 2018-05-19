import config
from structure_directory import StructureDirectory
from write_app import WriteApp


directory = config.CONFIGURATION['directory_path']
structure_directory_object = StructureDirectory(directory)
write_app_object = WriteApp()

if __name__ == '__main__':
    structure_directory_object.migrate_static()
    structure_directory_object.parse_html()
    write_app_object.write_app()
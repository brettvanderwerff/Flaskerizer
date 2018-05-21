from config import CONFIGURATION
from structure_directory import StructureDirectory
from write_app import WriteApp

structure_directory_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'],
                                                static_path=CONFIGURATION['static_path'])
write_app_object = WriteApp()

if __name__ == '__main__':
    structure_directory_object.migrate_static()
    structure_directory_object.parse_html()
    write_app_object.write_app()
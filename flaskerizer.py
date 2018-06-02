from Flaskerizer_src.config import CONFIGURATION
from Flaskerizer_src.structure_directory import StructureDirectory
from Flaskerizer_src.write_app import WriteApp

structure_directory_object = StructureDirectory(templates_path=CONFIGURATION['templates_path'],
                                                static_path=CONFIGURATION['static_path'],
                                                javascript_path=CONFIGURATION['javascript_path'])
write_app_object = WriteApp()

if __name__ == '__main__':
    structure_directory_object.migrate_static()
    structure_directory_object.parse_html()
    structure_directory_object.parse_javascript()
    write_app_object.write_app()
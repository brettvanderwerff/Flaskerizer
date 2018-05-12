import os
from structure_directory import StructureDirectory
from write_app import WriteApp

if __name__ == '__main__':
    flaskerizer_object = StructureDirectory(directroy=os.path.join(os.getcwd(), os.path.basename('Folio')))
    write_app_object = WriteApp()
    flaskerizer_object.migrate_static()
    flaskerizer_object.parse_html()
    write_app_object.write_app()
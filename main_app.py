from structure_directory import StructureDirectory
from write_app import WriteApp

flaskerizer_object = StructureDirectory(directroy=r'C:\Users\vande060\Desktop\coding\projects\Flaskerizer\Sailor')
write_app_object = WriteApp()

flaskerizer_object.migrate_static()
flaskerizer_object.parse_html()
write_app_object.write_app()
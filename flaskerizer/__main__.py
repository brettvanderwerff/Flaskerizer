from flaskerizer.flaskerizer_src.command_line_arguments import get_cmd_args
from flaskerizer.flaskerizer_src.structure_directory import StructureDirectory
from flaskerizer.flaskerizer_src.write_app import WriteApp

def main():
    '''The main method that runs the flaskerizer package.
    '''
    structure_directory_object = StructureDirectory(templates_path=get_cmd_args()['templates_path'],
                                                    top_level_path=get_cmd_args()['top_level_path'],
                                                    large_app_Structure=get_cmd_args()['large_app_structure'])

    structure_directory_object.structure_directory()
    write_app_object = WriteApp()
    if get_cmd_args()['large_app_structure'] == True:
        write_app_object.write_large_app()
    elif get_cmd_args()['large_app_structure'] == False:
        write_app_object.write_small_app()

if __name__ == "__main__":
    main()

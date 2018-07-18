import argparse
import flaskerizer.flaskerizer_src.examples.Alstar_example as example
import flaskerizer
import sys
import os


def get_command_line_arguments():
    '''
    Gets values from command line arguments, which are used to set configuration values in the flaskerizer_src/config.py
    script. Sets values to defaults if no command line arguments are given.
    '''
   
    parser = argparse.ArgumentParser(description='Flaskerizer: Convert Bootstrap templates to Flask apps')

    if os.path.basename(sys.argv[0]) == 'flaskerizer_app.py':

        parser.add_argument('--top-level-path', type=str, nargs=1, required=True,
                           help='Full path of the top level folder of the Bootstrap template')

        parser.add_argument('--templates-path', type=str, nargs=1,  required=True,
                           help='Full path of the folder containing the HTML files of the Bootstrap template')

    else: # workaround sets default '--top-level-path' and '--templates-path' values if file is not run from flaskerizer_app.py (i.e. testing)

        parser.add_argument('--top-level-path', type=str, nargs=1, default=[os.path.dirname(example.__file__)],
                            help='Full path of the top level folder of the Bootstrap template')

        parser.add_argument('--templates-path', type=str, nargs=1, default=[os.path.dirname(example.__file__)],
                            help='Full path of the folder containing the HTML files of the Bootstrap template')


    parser.add_argument('--app-name', type=str, nargs=1, default=['Flaskerized_app'],
                       help="Name of your Flask app, note cannot be named 'app'")

    parser.add_argument('--app-path', type=str, nargs=1,  default=[os.path.dirname(flaskerizer.__file__)],
                        help='Full path of the destination folder for your Flask app')

    parser.add_argument('--large-app-structure', dest='large_app_structure', action='store_true',
                       help='Create a Flask app with large package based structure')

    parser.add_argument('--no-large-app-structure', dest='large_app_structure', action='store_false',
                       help='Create a Flask app with a small module based structure')

    parser.set_defaults(large_app_structure=False)
    return vars(parser.parse_known_args()[0])


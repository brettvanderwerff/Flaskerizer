import argparse
import os
import sys
import flaskerizer.flaskerizer_src.examples.Alstar_example as example
import flaskerizer


def get_cmd_args():
    '''
    Gets values from command line arguments, which are used to set configuration values in the flaskerizer_src/config.py
    script. Sets values to defaults if no command line arguments are given.
    '''
    parser = argparse.ArgumentParser(description='Flaskerizer: Convert Bootstrap templates to Flask apps')
    if os.path.basename(sys.argv[0]) == 'flaskerizer' or os.path.basename(sys.argv[0]) == '__main__.py':

        parser.add_argument('--I', type=str, required=True, dest='top_level_path',
                            help='Full path of the top level folder of the Bootstrap template')

        parser.add_argument('--T', type=str, required=True, dest='templates_path',
                            help='Full path of the folder containing the HTML files of the Bootstrap template')

        parser.add_argument('--N', type=str, default='Flaskerized_app', dest='app_name',
                            help="Name of your Flask app, note cannot be named 'app'")

        parser.add_argument('--O', type=str, required=True, dest='app_path',
                            help='Full path of the destination folder for your Flask app')

        parser.add_argument('--L', dest='large_app_structure', action='store_true',
                            help='Create a Flask app with large package based structure')

        parser.add_argument('--S', dest='large_app_structure', action='store_false',
                            help='Create a Flask app with a small module based structure')

        parser.set_defaults(large_app_structure=False)

        if vars(parser.parse_known_args()[0])['app_name'] == 'app':
            print("The value of --N cannot be set to the string 'app'\n"
                  "Please change this configuration value to something valid like 'my_app' and try again")
            exit()


    else: # This is needed for when command_line_arguments.py is run by unit tests as a way to set default command line arguments
        parser.add_argument('--I', type=str, default=os.path.dirname(example.__file__), dest='top_level_path')

        parser.add_argument('--T', type=str, default=os.path.dirname(example.__file__), dest='templates_path')

        parser.add_argument('--N', type=str, default='Test_application', dest='app_name')

        parser.add_argument('--O', type=str, default=os.path.dirname(flaskerizer.__file__), dest='app_path')

        parser.add_argument('--L', default=True, dest='large_app_structure', action='store_true')


    return vars(parser.parse_known_args()[0])







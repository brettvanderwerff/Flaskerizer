import argparse


def get_cmd_args():
    '''
    Gets values from command line arguments, which are used to set configuration values in the flaskerizer_src/config.py
    script. Sets values to defaults if no command line arguments are given.
    '''

    parser = argparse.ArgumentParser(description='Flaskerizer: Convert Bootstrap templates to Flask apps')

    parser.add_argument('--top-level-path', type=str, required=True, dest='top_level_path',
                        help='Full path of the top level folder of the Bootstrap template')

    parser.add_argument('--templates-path', type=str,  required=True, dest='templates_path',
                        help='Full path of the folder containing the HTML files of the Bootstrap template')

    parser.add_argument('--app-name', type=str,  default='Flaskerized_app', dest='app_name',
                        help="Name of your Flask app, note cannot be named 'app'")

    parser.add_argument('--app-path', type=str,  required=True, dest='app_path',
                        help='Full path of the destination folder for your Flask app')

    parser.add_argument('--large-app-structure', dest='large_app_structure', action='store_true',
                        help='Create a Flask app with large package based structure')

    parser.add_argument('--no-large-app-structure', dest='large_app_structure', action='store_false',
                        help='Create a Flask app with a small module based structure')

    parser.set_defaults(large_app_structure=False)

    if vars(parser.parse_known_args()[0])['app_name'] == 'app':
        print("The value of --app-name cannot be set to the string 'app'\n"
              "Please change this configuration value to something valid like 'my_app' and try again")
        exit()

    return vars(parser.parse_known_args()[0])




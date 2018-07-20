import sys


def main(args=None):
    """The main routine."""
    parser = argparse.ArgumentParser(description='Flaskerizer: Convert Bootstrap templates to Flask apps')

    parser.add_argument('--top-level-path', type=str, nargs=1, required=True,
		   help='Full path of the top level folder of the Bootstrap template')

    parser.add_argument('--templates-path', type=str, nargs=1,  required=True,
		   help='Full path of the folder containing the HTML files of the Bootstrap template')

    parser.add_argument('--app-name', type=str, nargs=1, default=['Flaskerized_app'],
		   help="Name of your Flask app, note cannot be named 'app'")

    parser.add_argument('--app-path', type=str, nargs=1,  required=True,
		   help='Full path of the destination folder for your Flask app')

    parser.add_argument('--large-app-structure', dest='large_app_structure', action='store_true',
		  help='Create a Flask app with large package based structure')

    parser.add_argument('--no-large-app-structure', dest='large_app_structure', action='store_false',
		  help='Create a Flask app with a small module based structure')

if __name__ == "__main__":
    main()

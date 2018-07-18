from flaskerizer.flaskerizer_src.command_line_arguments import get_command_line_arguments

''' 
Config.py script sets configuration values in the CONFIGURATION dictionary to command line arguments if given.
If command line arguments are not given, these dictionary values are set to default values as described in
flaskerizer_src/command_line_arguments.py script
 
'''


CONFIGURATION = {
       'top_level_path' : get_command_line_arguments()['top_level_path'][0],
       'templates_path': get_command_line_arguments()['templates_path'][0],
       'large_app_structure' : get_command_line_arguments()['large_app_structure'],
       'app_name' : get_command_line_arguments()['app_name'][0], # app_name cannot be 'app'
       'app_path' : get_command_line_arguments()['app_path'][0]
}

if CONFIGURATION['app_name'] == 'app':
       print("The value of --app-name cannot be set to the string 'app'\n"
             "Please change this configuration value to something valid like 'my_app' and try again")
       exit()

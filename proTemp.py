import os
import sys
import sublime
import sublime_plugin
import functools


all_pro_info = sublime.active_window().extract_variables()
project_path = all_pro_info['folder']

def Window():
    '''Get current active window'''
    return sublime.active_window()

def get_project_name():
    '''Get project name'''

    project_data = sublime.active_window().project_data()
    project = os.path.basename(
        project_data['folders'][0]['path']) if project_data else None

    return project


def get_file_path(path):
    '''Get absolute path of the file'''

    return 'undefined' if path is None else path


def get_file_name(path):
    '''Get name of the file'''

    return 'undefined' if path is None else os.path.basename(path)


def get_file_name_without_extension(file_name):
    '''Get name of the file without extension'''

    return '.'.join(file_name.split('.')[:-1]) or file_name


def remove_project(project, module):
    '''Remove created project folders and files'''

    return  '''-'''+project+'''/json/'''+module+'''/getlist.js
            -'''+project+'''/json/'''+module+'''/add.js
            -'''+project+'''/json/'''+module+'''/delete.js
            -'''+project+'''/json/'''+module+'''/getedit.js
            -'''+project+'''/json/'''+module+'''/setedit.js
            -'''+project+'''/json/'''+module+'''/
            -'''+project+'''/json/
            -'''+project+'''/view/'''+module+'''/list.html
            -'''+project+'''/view/'''+module+'''/detail.html
            -'''+project+'''/view/'''+module+'''/
            -'''+project+'''/view/
            -'''+project+'''/
            -res/src/'''+project+'''/css/'''+module+'''/'''+module+'''.less
            -res/src/'''+project+'''/css/'''+module+'''/
            -res/src/'''+project+'''/css/
            -res/src/'''+project+'''/js/'''+module+'''/list.html
            -res/src/'''+project+'''/js/'''+module+'''/list.js
            -res/src/'''+project+'''/js/'''+module+'''/detail.html
            -res/src/'''+project+'''/js/'''+module+'''/detail.js
            -res/src/'''+project+'''/js/'''+module+'''/
            -res/src/'''+project+'''/js/
            -res/src/'''+project+'''/'''


def add_new_project(project, module):
    '''Create project folders and files'''
    return  project + '''/json(
                            ''' + module + '''/getlist.js
                            ''' + module + '''/saveadd.js
                            ''' + module + '''/delete.js
                            ''' + module + '''/getedit.js
                            ''' + module + '''/saveedit.js
                        )
                        ''' + project + '''/view(
                            ''' + module + '''/list.html
                            ''' + module + '''/detail.html
                        )
                        res/src/''' + project + '''/css/''' + module + '''/''' + module + '''.less
                        res/src/''' + project + '''/js(
                            ''' + module + '''/list.html
                            ''' + module + '''/list.js
                            ''' + module + '''/detail.html
                            ''' + module + '''/detail.js
                        )'''


def setProjectTree(args, args2):
    '''Set project folders and files'''
    le_solution = args2.split('/')[0]
    newModule = args2.split('/')[1]

    folders = sublime.active_window().project_data()
    print('get_project_name:'+get_project_name())
    from os.path import dirname, realpath
    print(dirname(realpath(__file__)))
    file_object = open( project_path + '/' + newModule + '.stprj', 'w')
    try:
        if le_solution[0] == '-':
            le_solution=le_solution.replace('-','')
            all_the_text = remove_project(le_solution, newModule)
        else:
            all_the_text = add_new_project(le_solution, newModule)
        file_object.write(all_the_text)
    finally:
        # file_object.flush( )
        file_object.close()
#endof setProjectTree

def delProjectConfig(arg1, file_name):
    '''Delete project config files'''
    print('print_filename:'+file_name)
    if file_name == '*':
        n = 0
        for root, dirs, files in os.walk(project_path + '/'):
            for name in files:
                if(name.endswith(".stprj")):
                    n += 1
                    os.remove(os.path.join(root, name))
    else:
        file_object = os.remove( project_path + '/' + file_name + '.stprj')
#endof delProjectConfig


class ProjectStprjUpdateFileCommand(sublime_plugin.TextCommand):
    '''Set project folders and files command'''
    Window().run_command('hide_panel')

    def run(a, b):
        Window().show_input_panel('Add/Remove Project:', 'project/module', functools.partial(
                                      setProjectTree, '')
                                 , None, None)


class projectDeleteConfigCommand(sublime_plugin.TextCommand):
    '''Delete project folders and files command'''
    Window().run_command('hide_panel')
    def run(a, b):
        Window().show_input_panel('Add/Remove Project:', '*', functools.partial(
                                      delProjectConfig, '')
                                 , None, None)



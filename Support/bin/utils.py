import textmate
# Import rope modules

def get_project(project_dir = textmate.PROJECT_DIRECTORY):
    """
    Returns a rope project for a given directory
    """
    try:
        from rope.base.project import Project
    except:
        textmate.exit_show_tool_tip('Rope module not found!')

    return Project(project_dir)
    

def get_auto_import(project, underlined = True):
    try:
        from rope.contrib.autoimport import AutoImport
    except:
        textmate.exit_show_tool_tip('Rope module not found!')

    autoimport = AutoImport(project, False, underlined)
    autoimport.generate_cache()
    return autoimport

    # if not proposals:
    #     project = get_project(textmate.PYTHONPATH + '/django')
    #     autoimport = AutoImport(project, False)
    #     autoimport.generate_cache()
    #     proposals = autoimport.import_assist(current_word)
    
    
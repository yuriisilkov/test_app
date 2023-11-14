import os
import json
import shutil
from datetime import datetime

root_dir = os.path.abspath(os.curdir)
new_app_path = f"{root_dir}/application.json"
app_folder_path = f"{root_dir}/application"


# Functions ----------------------------------------------------------------------------------------------------------


def get_new_app_version(file_path):
    # Get new app version
    with open(file_path, 'r') as f:
        file = json.load(f)
        version = file['version']
    return version


def deploy_new_app_version():
    shutil.copy(new_app_path, app_folder_path)
    unique_app_name = "Active_application.json"
    os.rename(f"{app_folder_path}/application.json", f"{app_folder_path}/{unique_app_name}")


def is_active_app_exist():
    if os.listdir(app_folder_path):
        for app_file in os.listdir(app_folder_path):
            if app_file == "Active_application.json":
                return True


def get_active_app_version():
    # Get active app version
    with open(f"{app_folder_path}/Active_application.json", 'r') as f:
        file = json.load(f)
        version = file['version']
    return version


def backup_active_app():
    today = datetime.today()
    current_time = today.strftime("%d_%m_%y_%H_%M_%S")
    old_name = "Active_application.json"
    new_name = f"{current_time}_application.json"
    os.rename(f"{app_folder_path}/{old_name}", f"{app_folder_path}/{new_name}")


# Scenario ------------------------------------------------------------------------------------------------------------

# Get new application version
new_app_version = get_new_app_version(new_app_path)


# Create application folder if not exist
if not os.path.isdir(app_folder_path):
    os.mkdir(app_folder_path)


# Verify that application folder is not empty
if not os.listdir(app_folder_path):
    # Deploy new application
    deploy_new_app_version()
else:
    # Verify that active application exist
    if is_active_app_exist():
        # Get active application version
        active_app_version = get_active_app_version()
        # Compare 'active application version' with 'new application version'
        if new_app_version != active_app_version:
            # Backup active application
            backup_active_app()
            # Deploy new application
            deploy_new_app_version()


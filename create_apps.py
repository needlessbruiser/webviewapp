import os
import json
import shutil
import logging

logging.basicConfig(filename='app_generation_errors.log', level=logging.ERROR)

# Constants
CONFIG_FILE_PATH = 'D:\\Ahsan Ghaffar\\Testing\\Web View App Code\\config.js'
BASE_PROJECT_DIRECTORY = "D:\\Ahsan Ghaffar\\Testing\\BaseAndroidApp"

def read_config_file():
    with open(CONFIG_FILE_PATH, 'r') as file:
        return json.load(file)

def setup_app_directory(app_name):
    base_dir = "D:\\Ahsan Ghaffar\\Testing\\Apps"
    new_dir = os.path.join(base_dir, app_name)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    shutil.copytree(BASE_PROJECT_DIRECTORY, new_dir, dirs_exist_ok=True)
    return new_dir  # Ensure this line is present and correctly returning the path

def setup_bundle_directories(app_dir):
    # Create the main directory 'abb and apk release'
    main_bundle_dir = os.path.join(app_dir, "abb and apk release")
    if not os.path.exists(main_bundle_dir):
        os.makedirs(main_bundle_dir)

    # Inside the main directory, create 'aab bundle' and 'apk bundle' directories
    aab_bundle_dir = os.path.join(main_bundle_dir, "aab bundle")
    apk_bundle_dir = os.path.join(main_bundle_dir, "apk bundle")

    if not os.path.exists(aab_bundle_dir):
        os.makedirs(aab_bundle_dir)

    if not os.path.exists(apk_bundle_dir):
        os.makedirs(apk_bundle_dir)        

    # The following line is redundant and should be removed
    # os.makedirs(app_dir)
    shutil.copytree(BASE_PROJECT_DIRECTORY, app_dir, dirs_exist_ok=True)
    return app_dir


def update_app_attributes(app_dir, config, app_icon_name):
    package_name = config['package_name']
    webview_url = config['webview_url']

    # Update Java package structure

    # Determine the path to the old directory
    old_java_dir_parts = ["app", "src", "main", "java"] + ["com", "taigameiolinehub", "taigameiolinehub"]
    old_java_dir = os.path.join(app_dir, *old_java_dir_parts)

    # Determine the path to the new directory
    new_java_dir_parts = ["app", "src", "main", "java"] + package_name.split('.')
    new_java_dir = os.path.join(app_dir, *new_java_dir_parts)

    # Check if the new directory already exists
    if os.path.exists(new_java_dir):
        shutil.rmtree(new_java_dir)  # Remove the existing directory

    #Now, rename the old directory to the new directory
    os.rename(old_java_dir, new_java_dir)

    # Update AndroidManifest.xml
    manifest_path = os.path.join(app_dir, "app\\src\\main\\AndroidManifest.xml")
    with open(manifest_path, 'r') as file:
        manifest_data = file.read()
    manifest_data = manifest_data.replace('com.taigameiolinehub.taigameiolinehub', package_name)
    manifest_data = manifest_data.replace('@drawable/taigameiolinehub', f'@drawable/{app_icon_name}')
    with open(manifest_path, 'w') as file:
        file.write(manifest_data)        

    # Update MainActivity.kt
    main_activity_path = os.path.join(new_java_dir, "MainActivity.kt")
    if os.path.exists(main_activity_path):
        with open(main_activity_path, 'r') as file:
            main_activity_data = file.read()
            main_activity_data = main_activity_data.replace('https://taigameionline.vn/', webview_url)
            main_activity_data = main_activity_data.replace('com.taigameiolinehub.taigameiolinehub', package_name)
        with open(main_activity_path, 'w') as file:
            file.write(main_activity_data)
    else:
        print(f"MainActivity.kt not found at {main_activity_path}")


    # Update build.gradle.kts
    build_gradle_path = os.path.join(app_dir, "app\\build.gradle.kts")
    with open(build_gradle_path, 'r') as file:
        build_data = file.read()
    build_data = build_data.replace('com.taigameiolinehub.taigameiolinehub', package_name)
    with open(build_gradle_path, 'w') as file:
        file.write(build_data)

    # Update settings.gradle.kts
    settings_gradle_path = os.path.join(app_dir, "settings.gradle.kts")
    with open(settings_gradle_path, 'r') as file:
        settings_data = file.read()
    settings_data = settings_data.replace('Taigameioline Hub', config['app_name'])
    with open(settings_gradle_path, 'w') as file:
        file.write(settings_data)

    # Update app_name in strings.xml
    strings_xml_path = os.path.join(app_dir, "app\\src\\main\\res\\values\\strings.xml")
    with open(strings_xml_path, 'r') as file:
        strings_data = file.read()

    app_name_tag = '<string name="app_name">'
    end_tag = '</string>'
    start_index = strings_data.find(app_name_tag) + len(app_name_tag)
    end_index = strings_data.find(end_tag, start_index)
    strings_data = strings_data[:start_index] + config['app_name'] + strings_data[end_index:]

    with open(strings_xml_path, 'w') as file:
        file.write(strings_data)

def handle_app_resources(app_dir, app_icon):
    destination_icon_path = os.path.join(app_dir, "app\\src\\main\\res\\drawable")
    shutil.copy(app_icon, destination_icon_path)
    # Remove old icon
    old_icon_path = os.path.join(destination_icon_path, "taigameiolinehub.png")
    if os.path.exists(old_icon_path):
        os.remove(old_icon_path)

    # Load signing configuration
with open('signing_config.json', 'r') as file:
    signing_config_data = json.load(file)

KEYSTORE_PATH = signing_config_data['keystorePath']
KEY_ALIAS = signing_config_data['keyAlias']    

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)        

def sync_with_gradle(app_dir):
    os.chdir(app_dir)
    os.system('gradlew.bat --refresh-dependencies')

def clean_project(app_dir):
    os.chdir(app_dir)
    os.system('gradlew clean')

def rebuild_project(app_dir):
    os.chdir(app_dir)
    os.system('gradlew build')

# Centralized keystore path
KEYSTORE_PATH = "D:\\Ahsan Ghaffar\\Testing\\BaseAndroidApp\\keys\\centralized_keystore.jks"

# def get_password(prompt_text):
#     """Prompt the user to enter a password without echoing."""
#     import getpass
#     return getpass.getpass(prompt_text)

# def build_and_compile(app_dir, app_name):
#     os.chdir(app_dir)
    
#     # Get keystore passwords from the user
#     store_password = get_password(f"Enter the store password for {app_name}: ")
#     key_password = get_password(f"Enter the key password for {app_name}: ")

#     # Modify build.gradle.kts to include signingConfig for release
#     build_gradle_path = os.path.join(app_dir, "app\\build.gradle.kts")
#     signing_config = f'''
#     signingConfigs {{
#         release {{
#             storeFile file('{KEYSTORE_PATH}')
#             storePassword '{store_password}'
#             keyAlias '{app_name}'
#             keyPassword '{key_password}'
#         }}
#     }}
#     '''
#     with open(build_gradle_path, 'a') as file:
#         file.write(signing_config)
    
#     # Build APK and AAB with the signing config
#     os.system('gradlew assembleRelease')  # Build APK
#     os.system('gradlew bundleRelease')    # Build AAB

# def move_bundles(app_name, app_dir):
#     ensure_directory_exists(f"{app_dir}/abb_and_apk_release_bundle/abb_bundle/")
#     ensure_directory_exists(f"{app_dir}/abb_and_apk_release_bundle/apk_bundle/")
    
#     source_aab_path = f"{app_dir}/app/build/outputs/bundle/release/{app_name}.aab"
#     destination_aab_path = f"{app_dir}/abb_and_apk_release_bundle/abb_bundle/{app_name}.aab"
#     shutil.move(source_aab_path, destination_aab_path)
    
#     source_apk_path = f"{app_dir}/app/build/outputs/apk/release/{app_name}.apk"
#     destination_apk_path = f"{app_dir}/abb_and_apk_release_bundle/apk_bundle/{app_name}.apk"
#     shutil.move(source_apk_path, destination_apk_path)


def main():
    configs = read_config_file()
    for config in configs:
        app_name = config['app_name']
        app_dir = setup_app_directory(config['app_name'])
        
        setup_bundle_directories(app_dir)  # Call the function here
        
        app_icon_name = os.path.basename(config['app_icon']).split('.')[0]
        update_app_attributes(app_dir, config, app_icon_name)
        handle_app_resources(app_dir, config['app_icon'])

        # Sync, clean, rebuild, and compile
        sync_with_gradle(app_dir)
        clean_project(app_dir)
        rebuild_project(app_dir)

        # Removed generate_encrypted_key as we're using a centralized keystore
        # build_and_compile(app_dir, app_name)
        # move_bundles(app_name, app_dir)

if __name__ == '__main__':
    main()

    

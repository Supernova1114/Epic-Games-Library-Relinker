import sys
import os

DEFAULT_MANIFESTS_PATH: str = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"

def print_line_separator() -> None:
    print('-' * 40)

def assert_path_exists(path: str) -> None:
    if os.path.exists(path) == False:
        print("Error: Path does not exist!")
        exit(0)

def main():

    print("dont run")
    sys.exit(0)

    # Get Epic Games store manifests path ------------------------------------
   
    launcher_manifests_path: str = ""

    print("Default Manifests Path: ", DEFAULT_MANIFESTS_PATH)

    option: str = input("Use default manifests path? (y/n): ")
    if str.upper(option[0]) == 'Y':
        launcher_manifests_path = DEFAULT_MANIFESTS_PATH
    else:
        launcher_manifests_path = input("Please input a valid path: ")

    assert_path_exists(launcher_manifests_path)

    # Get game data path ----------------------------------------------------
    
    # game_data_path: str = input("Please enter parent folder path containing all games: ")
    # assert_path_exists(game_data_path)

    # TODO - TEMP REMOVE LINES
    game_data_path = "F:\\Program Files\\Epic Games"
    assert_path_exists(game_data_path)

    # Get list of game folder paths ------------------------------------------

    game_path_list: list[str] = []

    for entry in os.scandir(game_data_path):
        game_path_list.append(entry.path)

    # Get list of manifest file paths ----------------------------------------

    launcher_manifest_file_list: list[str] = []
    
    manifest_file_type = ".item"

    for entry in os.scandir(launcher_manifests_path):
        if entry.is_file() and manifest_file_type in entry.name:
            launcher_manifest_file_list.append(entry.path)

    # Print results ----------------------------------------------------------

    print("Games Found: ", len(game_path_list))
    print("Manifest Files Found: ", len(launcher_manifest_file_list))

    exit(0)

    # Get config value for detecting duplicates ------------------------------

    # List of tuples containing game name and manifest file path
    # list[tuple[game_name, manifest_file_path]]
    manifest_game_list: list[tuple[str, str]] = []

    for filepath in launcher_manifest_file_list:
        with open(filepath, "r") as manifest_file:
            while True:
                line = manifest_file.readline().rstrip()
                config_entry = line.split(":")

                if "MandatoryAppFolderName" in config_entry[0]:
                    manifest_game_list.append((config_entry[1][2:-2], filepath))
                    break
    
    # Put duplicates together for later removal ------------------------------

    duplicate_manifests_dict: dict[str, list[tuple[str, str]]] = {}

    # entry: tuple[game_name, manifest_file_path]
    for entry in manifest_game_list:
        game_name = entry[0]

        if duplicate_manifests_dict.get(game_name) == None: 
            duplicate_manifests_dict[game_name] = [entry]
        else:
            duplicate_manifests_dict[game_name].append(entry)

    manifests_dict_values = duplicate_manifests_dict.values()

    # Print duplicates -------------------------------------------------------
            
    print_line_separator()

    for duplicate_manifests_list in manifests_dict_values:
        if len(duplicate_manifests_list) > 1:
            game_name = duplicate_manifests_list[0][0]
            print(f"Duplicate Manifests ({game_name}): {len(duplicate_manifests_list)}")

    print_line_separator()

    # Find the most recent duplicate manifest file for each game -------------

    recent_manifest_list: list[tuple[str, str]] = []

    # duplicate_manifests_list: list[tuple[game_name, manifest_file_path]]
    for duplicate_manifests_list in manifests_dict_values:
        if len(duplicate_manifests_list) > 1: # We know there are duplicates
            
            most_recent_manifest: tuple[str, str] = duplicate_manifests_list[0] 
            most_recent_mod_time: int = os.stat(most_recent_manifest[1]).st_mtime_ns

            for duplicate_manifest in duplicate_manifests_list:
                file_modified_time = os.stat(duplicate_manifest[1]).st_mtime_ns

                if file_modified_time > most_recent_mod_time:
                    most_recent_mod_time = file_modified_time
                    most_recent_manifest = duplicate_manifest

            recent_manifest_list.append(most_recent_manifest)


    # TODO scan for InstallationGuid config entry/manifest name in both program data and game folder.

    # Remove older duplicate manifest files ----------------------------------

    option: str = input("Remove old duplicate manifest files? (y/n): ")
    
    if str.upper(option[0]) == 'Y':
        
        for recent_manifest in recent_manifest_list:
            duplicate_manifest_list = duplicate_manifests_dict.get(recent_manifest[0])
            
            for duplicate_manifest in duplicate_manifest_list:
                if duplicate_manifest != recent_manifest:
                    print(f"Removing Manifest ({duplicate_manifest[0]}) at {duplicate_manifest[1]}")
                    os.remove(duplicate_manifest[1])

    # Relink game folders to most recent manifest files ----------------------
            
    option: str = input("Relink game folders to manifest files? (y/n): ")

    if str.upper(option[0]) == 'Y':
            
            ...
            # TODO - finish this up
            # Go through each manifest file, find the game folder path
            # If the actual game folder path is different than the one in the manifest file
            # Then update the manifest file with the new game folder path:
            #   - Find the line containing the game folder path
            #   - Replace the line with the new game folder path


            # Some new notes
            # - Will not be able to directly download manifest file.
            # - User will have to manually begin installation in order for the store to create the file
            # - Once the file is created, the user must cancel the installation, then run this script.
            # - This script will update the manifest file name to match the guid of the manifest in the game folder.
            # - It will also update the game folder paths in the manifest file to match the actual game folder path, and guid.
            # - The manifest file will be moved to the non pending folder, right after stopping the install using this script.
            


if __name__ == "__main__":
    main()

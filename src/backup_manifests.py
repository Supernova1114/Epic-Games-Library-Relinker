import os
import sys
import shutil

DEFAULT_MANIFESTS_PATH: str = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"
MANIFEST_BACKUP_FOLDER_NAME: str = "_MANIFEST_BACKUPS"

def print_line_separator() -> None:
    print('-' * 40)

def assert_path_exists(path: str) -> None:
    if os.path.exists(path) == False:
        print("ERROR!: Path does not exist!")
        sys.exit(0)

def yes_no_prompt(prompt: str) -> bool:
    option: str = input(f"PROMPT: {prompt} (y/n): ")
    return len(option) != 0 and str.upper(option[0]) == 'Y'

def main():

    # Get Epic Games store manifests path ------------------------------------
   
    launcher_manifests_path: str = ""

    print("INFO: Default Manifests Path: ", DEFAULT_MANIFESTS_PATH)

    if yes_no_prompt("Use default manifests path?"):
        launcher_manifests_path = DEFAULT_MANIFESTS_PATH
    else:
        launcher_manifests_path = input("PROMPT: Please input a valid path: ")

    assert_path_exists(launcher_manifests_path)

    # Get game data path ----------------------------------------------------
    
    game_data_path: str = input("PROMPT: Please enter parent folder path containing all games: ")
    assert_path_exists(game_data_path)

    # TODO - TEMP REMOVE LINES
    # game_data_path = "F:\\Program Files\\Epic Games"
    # assert_path_exists(game_data_path)

    # Get list of launcher manifest file paths -------------------------------

    launcher_manifest_file_list: list[os.DirEntry] = []
    
    launcher_manifest_file_type = ".item"

    for lm_entry in os.scandir(launcher_manifests_path):
        if lm_entry.is_file() and launcher_manifest_file_type in lm_entry.name:
            launcher_manifest_file_list.append(lm_entry)

    # Get game folder list and game manifest list ----------------------------

    game_folder_list: list[os.DirEntry] = []

    game_manifest_file_list: list[os.DirEntry] = []
    game_manifest_file_type = ".manifest"

    print_line_separator()

    for game_folder_entry in os.scandir(game_data_path):

        if not game_folder_entry.is_dir() or game_folder_entry.name == MANIFEST_BACKUP_FOLDER_NAME:
            continue

        game_manifest_folder = os.path.join(game_folder_entry.path, ".egstore")

        if os.path.exists(game_manifest_folder) == False:
            print(f"WARNING!: Skipping \"{game_folder_entry.name}/\" as it does not contain \".egstore/\"")
            continue
        
        found_manifest = False

        for gm_entry in os.scandir(game_manifest_folder):
            if (gm_entry.is_file() and game_manifest_file_type in gm_entry.name):
                game_manifest_file_list.append(gm_entry)
                found_manifest = True

        if found_manifest:
            print(f"INFO: Adding \"{game_folder_entry.name}\"")
            game_folder_list.append(game_folder_entry)
        else:
            print(f"WARNING!: Skipping \"{game_folder_entry.name}/.egstore/\" as it is missing a game manifest file. (May be an incomplete installation).")

    print_line_separator()

    if len(game_folder_list) == 0:
        print(f"ERROR!: No games found! Aborting...")
        sys.exit(1)

    # Backup launcher manifest files -----------------------------------------

    manifest_backup_folder = os.path.join(game_data_path, MANIFEST_BACKUP_FOLDER_NAME)

    if yes_no_prompt(f"Launcher manifests will backup to \"{manifest_backup_folder}\". Continue?") == False:
        print("INFO: Aborting...")
        sys.exit(0)

    print_line_separator()

    if os.path.exists(manifest_backup_folder) == False:
        print(f"INFO: Creating folder: {manifest_backup_folder}")
        os.mkdir(manifest_backup_folder)

    for gm_file in game_manifest_file_list:
        gm_name, _ = os.path.splitext(gm_file.name) # Game manifest

        lm_found = False
        
        for lm_file in launcher_manifest_file_list:
            lm_name, _ = os.path.splitext(lm_file.name) # Launcher manifest
    
            if gm_name == lm_name:
                lm_found = True
                # TODO - print out game name instead.
                print(f"INFO: Backing up \"{lm_file.name}\".")
                shutil.copy2(lm_file.path, manifest_backup_folder)    

        if lm_found == False:
            # TODO - print out game name instead.
            print(f"WARNING: Unable to backup launcher manifest for \"{gm_file.name}\". (Launcher manifest does not exist).")

    print_line_separator()

    sys.exit(0)


if __name__ == "__main__":
    main()
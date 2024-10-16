import os
import sys
import shutil

DEFAULT_MANIFESTS_PATH: str = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"
MANIFEST_BACKUP_FOLDER_NAME: str = "_manifest_backups"

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

    # Restore all launcher manifests ---------------------------------------------------

    if yes_no_prompt("Ready to restore launcher manifests. Continue?"):
        launcher_manifests_path = DEFAULT_MANIFESTS_PATH
    else:
        launcher_manifests_path = input("PROMPT: Please input a valid path: ")

    manifest_backup_folder = os.path.join(game_data_path, MANIFEST_BACKUP_FOLDER_NAME)

    launcher_manifest_file_type = ".item"

    for entry in os.scandir(manifest_backup_folder):
        if entry.is_file() and launcher_manifest_file_type in entry.name:
            print(f"INFO: Restoring launcher manifest: {entry.name}")
            shutil.copy2(entry.path, launcher_manifests_path)


if __name__ == "__main__":
    main()
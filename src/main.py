import os
import sys
import shutil
from dataclasses import dataclass

DEFAULT_MANIFESTS_PATH: str = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"
MANIFEST_BACKUP_FOLDER_NAME: str = "_MANIFEST_BACKUPS"

GAME_MANIFEST_FOLDER_NAME: str = ".egstore"
GAME_MANIFEST_FILE_TYPE: str = ".manifest"
LAUNCHER_MANIFEST_FILE_TYPE: str = ".item"


@dataclass
class FileDirectory:
    name: str # Name of file or folder.
    path: str # Path to file or folder.

    def get_name_raw(self) -> str:
        return os.path.splitext(self.name)[0]
    
    def get_extension(self) -> str:
        return os.path.splitext(self.name)[1]

@dataclass
class GameData:
    game_folder: FileDirectory
    manifest_folder: FileDirectory
    manifest_file_list: list[FileDirectory]


def print_line_separator() -> None:
    print('-' * 40)

def assert_path_exists(path: str) -> None:
    if os.path.exists(path) == False:
        print("ERROR!: Path does not exist!")
        sys.exit(0)

def yes_no_prompt(prompt: str) -> bool:
    option: str = input(f"{prompt} (y/n): ")
    return len(option) != 0 and str.upper(option[0]) == 'Y'

def is_valid_launcher_manifest_file(entry: os.DirEntry) -> bool:
    return (
        entry.is_file() 
        and LAUNCHER_MANIFEST_FILE_TYPE in entry.name
    )

def is_valid_game_manifest_file(entry: os.DirEntry) -> bool:
    return (
        entry.is_file() 
        and GAME_MANIFEST_FILE_TYPE in entry.name
    )

def is_valid_game_folder(entry: os.DirEntry) -> bool:
    return (
        entry.is_dir() 
        and entry.name != MANIFEST_BACKUP_FOLDER_NAME
        and os.path.exists(os.path.join(entry.path, GAME_MANIFEST_FOLDER_NAME))
    )

def get_launcher_manifest_files(launcher_manifests_path: str) -> list[FileDirectory]:
    
    launcher_manifest_file_list: list[FileDirectory] = []

    for manifest_entry in os.scandir(launcher_manifests_path):
        if is_valid_launcher_manifest_file(manifest_entry):
            launcher_manifest_file_list.append(FileDirectory(manifest_entry.name, manifest_entry.path))
    
    return launcher_manifest_file_list

def get_game_data_list(game_data_path: str):
    
    game_data_list: list[GameData] = []
    
    for game_entry in os.scandir(game_data_path):
        
        game_folder: FileDirectory = None
        manifest_folder: FileDirectory = None
        manifest_file_list: list[FileDirectory] = []

        if is_valid_game_folder(game_entry) == False:
            print(f"WARNING!: Skipping \"{game_entry.name}/\" as it is not a valid game folder.")
            continue

        manifest_folder_path = os.path.join(game_entry.path, GAME_MANIFEST_FOLDER_NAME)

        for manifest_entry in os.scandir(manifest_folder_path):
            if is_valid_game_manifest_file(manifest_entry):
                manifest_file_list.append(FileDirectory(manifest_entry.name, manifest_entry.path))
        
        if len(manifest_file_list) == 0:
            print(f"WARNING!: Skipping \"{game_entry.name}/.egstore/\" as it is missing a manifest file. (May be an incomplete installation).")
            continue
        
        game_folder = FileDirectory(game_entry.name, game_entry.path)
        manifest_folder = FileDirectory(GAME_MANIFEST_FOLDER_NAME, manifest_folder_path)

        print(f"INFO: Adding \"{game_entry.name}\"")
        game_data_list.append(GameData(game_folder, manifest_folder, manifest_file_list))

    # END for

    return game_data_list

def backup_game_manifest_files(
    manifest_backup_folder: str, 
    launcher_manifest_file_list: list[FileDirectory], 
    game_data_list: list[GameData] 
    ) -> None:

    for game_data in game_data_list:
        for game_manifest in game_data.manifest_file_list:
            
            # Find launcher manifest that matches the name of the game manifest.
            # Search result is None if match does not exist.
            # Assumes there is only one or zero matching launcher manifests.
            matching_launcher_manifest: FileDirectory = next(
                (launcher_manifest for launcher_manifest in launcher_manifest_file_list if game_manifest.get_name_raw() == launcher_manifest.get_name_raw()),
                None
            )

            if matching_launcher_manifest is not None:
                print(f"INFO: Backing up \"{matching_launcher_manifest.name}\".")
                shutil.copy2(matching_launcher_manifest.path, manifest_backup_folder)    
            else:
                print(f"WARNING: Unable to backup launcher manifest for \"{game_data.game_folder.name}\". (Launcher manifest does not exist).")

def restore_manifests(manifest_backup_folder: str, launcher_manifest_folder: str) -> None:

    if yes_no_prompt(f"Launcher manifests will restore to \"{launcher_manifest_folder}\". Continue?") == False:
        print("INFO: Aborting...")
        sys.exit(0)

    print_line_separator()

    for entry in os.scandir(manifest_backup_folder):
        if entry.is_file() and LAUNCHER_MANIFEST_FILE_TYPE in entry.name:
            print(f"INFO: Restoring launcher manifest: {entry.name}")
            shutil.copy2(entry.path, launcher_manifest_folder)
    
    print_line_separator()

def backup_manifests(launcher_manifest_folder: str, manifest_backup_folder: str, game_data_list: str) -> None:
    
    if yes_no_prompt(f"Launcher manifests will backup to \"{manifest_backup_folder}\". Continue?") == False:
        print("INFO: Aborting...")
        sys.exit(0)

    print_line_separator()

    if os.path.exists(manifest_backup_folder) == False:
        print(f"INFO: Creating folder: {manifest_backup_folder}")
        os.mkdir(manifest_backup_folder)

    launcher_manifest_file_list: list[FileDirectory] = get_launcher_manifest_files(launcher_manifest_folder)

    backup_game_manifest_files(manifest_backup_folder, launcher_manifest_file_list, game_data_list)

    print_line_separator()


def main():

    # Get Epic Games store manifests path ------------------------------------
   
    launcher_manifest_folder: str = ""

    print("Welcome to Epic Games Relinker")
    print_line_separator()
    print(f"INFO: Default Manifests Path: {DEFAULT_MANIFESTS_PATH}")
    print_line_separator()

    if yes_no_prompt("Use default manifests path?"):
        launcher_manifest_folder = DEFAULT_MANIFESTS_PATH
    else:
        launcher_manifest_folder = input("Please input a valid path: ")

    assert_path_exists(launcher_manifest_folder)

    # Get game data path ----------------------------------------------------
    
    game_data_path: str = input("Please enter games folder path: ")
    assert_path_exists(game_data_path)

    # Get game folder list and game manifest list ----------------------------

    print_line_separator()
    game_data_list: list[GameData] = get_game_data_list(game_data_path)
    print_line_separator()

    if len(game_data_list) == 0:
        print(f"ERROR!: No games found! Aborting...")
        sys.exit(1)

    menu_prompt = "1. Backup Manifests\n2. Restore Manifests\nEnter an option: "
    option: int = int(input(menu_prompt))

    print_line_separator()

    manifest_backup_folder = os.path.join(game_data_path, MANIFEST_BACKUP_FOLDER_NAME)

    match (option):
        case 1:
            backup_manifests(launcher_manifest_folder, manifest_backup_folder, game_data_list)
        case 2:
            restore_manifests(manifest_backup_folder, launcher_manifest_folder)
        case _:
            print("WARNING: Invalid option!")

    print("INFO: Process Complete! Exiting...")
    sys.exit(0)


if __name__ == "__main__":
    main()
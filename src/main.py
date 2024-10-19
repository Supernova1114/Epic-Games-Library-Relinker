import os
import sys
import shutil
import json
from dataclasses import dataclass

DEFAULT_MANIFESTS_PATH: str = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"
MANIFEST_BACKUP_FOLDER_NAME: str = "_MANIFEST_BACKUPS"

GAME_MANIFEST_FOLDER_NAME: str = ".egstore"
GAME_MANIFEST_FILE_TYPE: str = ".manifest"

STAGING_FOLDER_NAME: str = "bps"

LAUNCHER_MANIFEST_FILE_TYPE: str = ".item"
SUPPORTED_LAUNCHER_MANIFEST_VERSIONS: list[int] = [0,]

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

def assert_path_exists(path: str, hint: str = "") -> None:
    if os.path.exists(path) == False:
        print(f"ERROR!: Path does not exist! \"{path}\"")

        if len(hint) != 0:
            print(f"ERROR!: {hint}")

        sys.exit(1)

def try_create_dir(path: str) -> None:
    if os.path.exists(path) == False:
        print(f"INFO: Creating folder: {path}")
        os.mkdir(path)

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

def get_matching_launcher_manifest(
    game_manifest: FileDirectory,
    launcher_manifest_file_list: list[FileDirectory]
) -> FileDirectory:
    
    # Find launcher manifest that matches the name of the game manifest.
    # Search result is None if match does not exist.
    # Assumes there is only one or zero matching launcher manifests.
    matching_launcher_manifest: FileDirectory = next(
        (launcher_manifest for launcher_manifest in launcher_manifest_file_list if game_manifest.get_name_raw() == launcher_manifest.get_name_raw()),
        None # Default
    )

    return matching_launcher_manifest

def assert_manifest_is_supported(format_version: int):

    if format_version not in SUPPORTED_LAUNCHER_MANIFEST_VERSIONS:

        output: str = "ERROR!: Launcher manifest format version is incompatible.\n"
        output += "Check if the new launcher \".item\" manifest format is compatible with this program.\n"
        output += "Then add format version to SUPPORTED_LAUNCHER_MANIFEST_VERSIONS." 

        print(output)
        sys.exit(1)

def update_manifest_location_references(launcher_manifest: FileDirectory, game_folder_path: str) -> None:

    # TODO - Add check if relinking is actually necessary or not.

    # Open file as read/write
    with open(launcher_manifest.path, 'r+') as file:
        data = json.load(file)

        # Check version
        assert_manifest_is_supported(data["FormatVersion"])

        manifest_location = os.path.join(game_folder_path, GAME_MANIFEST_FOLDER_NAME)
        staging_location = os.path.join(manifest_location, STAGING_FOLDER_NAME)

        # Update location references
        data["InstallLocation"] = game_folder_path
        data["ManifestLocation"] = manifest_location
        data["StagingLocation"] = staging_location

        file.seek(0) # Reset file pointer to beginning.
        json.dump(data, file, indent=4) #
        file.truncate() # Remove any remaining data after the written data.
    
def backup_game_manifest_files(
    manifest_backup_folder: str, 
    launcher_manifest_file_list: list[FileDirectory], 
    game_data_list: list[GameData] 
) -> None:

    for game_data in game_data_list:
        for game_manifest in game_data.manifest_file_list:
            
            matching_launcher_manifest: FileDirectory = get_matching_launcher_manifest(game_manifest, launcher_manifest_file_list)

            if matching_launcher_manifest is not None:
                print(f"INFO: Backing up \"{matching_launcher_manifest.name}\".")
                shutil.copy2(matching_launcher_manifest.path, manifest_backup_folder)    
            else:
                print(f"WARNING: Unable to backup launcher manifest for \"{game_data.game_folder.name}\". (Launcher manifest does not exist).")

def restore_manifests(manifest_backup_folder: str, launcher_manifest_folder: str) -> None:

    assert_path_exists(manifest_backup_folder, hint="You may need to backup manifests first.")

    if yes_no_prompt(f"Launcher manifests will restore to \"{launcher_manifest_folder}\". Continue?") == False:
        print("INFO: Aborting...")
        sys.exit(0)

    print_line_separator()

    for manifest_entry in os.scandir(manifest_backup_folder):
        if is_valid_launcher_manifest_file(manifest_entry):
            print(f"INFO: Restoring launcher manifest: {manifest_entry.name}")
            shutil.copy2(manifest_entry.path, launcher_manifest_folder)
    
    print_line_separator()

def backup_manifests(manifest_backup_folder: str, launcher_manifest_folder: str, game_data_list: list[GameData]) -> None:
    
    if yes_no_prompt(f"Launcher manifests will backup to \"{manifest_backup_folder}\". Continue?") == False:
        print("INFO: Aborting...")
        sys.exit(0)

    print_line_separator()

    try_create_dir(manifest_backup_folder)

    launcher_manifest_file_list: list[FileDirectory] = get_launcher_manifest_files(launcher_manifest_folder)

    backup_game_manifest_files(manifest_backup_folder, launcher_manifest_file_list, game_data_list)

    print_line_separator()

def move_game_installation(manifest_backup_folder: str, game_data_list: list[GameData]) -> None:
    
    assert_path_exists(manifest_backup_folder, hint="You may need to backup manifests first.")

    print("Movable Games Menu:")

    # Print out menu for game selection
    for index, game_data in enumerate(game_data_list):
        print(f"{index + 1}. {game_data.game_folder.name}")

    print()

    selection_raw = input("Select games to move (Comma separated, EX: 1,2,3): ")
    selection_list = selection_raw.strip().split(",")

    selected_games_list: list[GameData] = []

    for selection_str in selection_list:
        selection_index: int = int(selection_str) - 1

        if selection_index < 0 or selection_index >= len(game_data_list):
            print(f"ERROR!: Invalid option \"{selection_index + 1}\"")
            sys.exit(1)

        selected_games_list.append(game_data_list[selection_index])

    print_line_separator()

    # Print out what user selected
    print("Your selection:")
    for selected_game in selected_games_list:
        print(f"- \"{selected_game.game_folder.name}\"")

    print_line_separator()    

    destination_path: str = input("Input a destination path: ")
    assert_path_exists(destination_path)
    
    print_line_separator()

    prompt = f"Selected game installations will be moved to \"{destination_path}\".\n"
    prompt += f"Folder \"{MANIFEST_BACKUP_FOLDER_NAME}/\" will be created.\n"
    prompt += "Associated manifest files will be moved.\n"
    prompt += "Manifest file location references will be updated.\nContinue?"

    if yes_no_prompt(prompt) == False:
        print("INFO: Aborting...")
        sys.exit(0)

    print_line_separator()

    # Create manifest backups folder in destination folder.
    destination_backup_folder = os.path.join(destination_path, MANIFEST_BACKUP_FOLDER_NAME)
    try_create_dir(destination_backup_folder)

    launcher_manifest_file_list: list[FileDirectory] = get_launcher_manifest_files(manifest_backup_folder)

    for selected_game in selected_games_list:

        found_all_manifests = True

        # Find matching launcher manifests within the backups folder.
        for game_manifest in selected_game.manifest_file_list:
            matching_launcher_manifest = get_matching_launcher_manifest(game_manifest, launcher_manifest_file_list)

            if matching_launcher_manifest is None:
                found_all_manifests = False
                break

            # Update launcher manifest with new destination
            new_game_folder_path: str = os.path.join(destination_path, selected_game.game_folder.name)
            update_manifest_location_references(matching_launcher_manifest, new_game_folder_path)

            # Move launcher manifest to destination
            shutil.move(matching_launcher_manifest.path, destination_backup_folder)

        if found_all_manifests == True:
            # Move game installation
            print(f"INFO: Moving game \"{selected_game.game_folder.name}\"")
            shutil.move(selected_game.game_folder.path, destination_path)
        else:
            print(f"WARNING!: Skipping \"{selected_game.game_folder.name}\" as it is missing a manifest file within {MANIFEST_BACKUP_FOLDER_NAME}")

    print_line_separator()

    # TODO - Add suggestion to restore updated launcher manifests.

def relink_manifests(manifest_backup_folder: str, game_data_list: list[GameData]) -> None:

    prompt: str = f"Launcher manifests within \"{manifest_backup_folder}\""
    prompt += " will be relinked to their associated games.\nContinue?"
    
    if yes_no_prompt(prompt) == False:
        print("INFO: Aborting...")
        sys.exit(0)

    launcher_manifest_file_list: list[FileDirectory] = get_launcher_manifest_files(manifest_backup_folder)

    for game_data in game_data_list:
        for game_manifest in game_data.manifest_file_list:
            matching_launcher_manifest: FileDirectory = get_matching_launcher_manifest(game_manifest, launcher_manifest_file_list)

            if matching_launcher_manifest is None:
                print(f"WARNING!: Launcher manifest for \"{game_data.game_folder.name}\" matching {game_manifest.name} does not exist.")
                continue

            # Update launcher manifest to reference correct game path.
            print(f"INFO: Relinking \"{game_data.game_folder.name}\"")
            update_manifest_location_references(matching_launcher_manifest, game_data.game_folder.path)

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

    menu_prompt: str = "Main Menu:\n"
    menu_prompt += "1. Backup Manifests\n2. Restore Manifests\n"
    menu_prompt += "3. Move Game Installation\n4. Relink Manifests\n"
    menu_prompt += "0. Exit"

    print(menu_prompt)

    option: int = int(input("Enter an option: "))

    print_line_separator()

    manifest_backup_folder = os.path.join(game_data_path, MANIFEST_BACKUP_FOLDER_NAME)

    match (option):
        case 0:
            print("INFO: Exiting...")
            sys.exit(0)
        case 1:
            backup_manifests(manifest_backup_folder, launcher_manifest_folder, game_data_list)
        case 2:
            restore_manifests(manifest_backup_folder, launcher_manifest_folder)
        case 3:
            move_game_installation(manifest_backup_folder, game_data_list)
        case 4:
            relink_manifests(manifest_backup_folder, game_data_list)
        case _:
            print("WARNING: Invalid option!")

    print("INFO: Process Complete! Exiting...")
    sys.exit(0)


if __name__ == "__main__":
    main()
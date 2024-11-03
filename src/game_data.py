from dataclasses import dataclass
from file_management import FileDirectory
import os
import sys

@dataclass
class GameData:
    game_folder: FileDirectory
    manifest_folder: FileDirectory
    manifest_file_list: list[FileDirectory]

@dataclass
class GameDataManager:
    game_data_list: list[GameData] = []


    @staticmethod
    def is_valid_game_folder(entry: os.DirEntry) -> bool:
        return (
            entry.is_dir() 
            and entry.name != MANIFEST_BACKUP_FOLDER_NAME
            and os.path.exists(os.path.join(entry.path, GAME_MANIFEST_FOLDER_NAME))
        )
    
    @staticmethod
    def is_valid_launcher_manifest_file(entry: os.DirEntry) -> bool:
        return (
            entry.is_file() 
            and LAUNCHER_MANIFEST_FILE_TYPE in entry.name
        )
    
    @staticmethod
    def is_valid_game_manifest_file(entry: os.DirEntry) -> bool:
        return (
            entry.is_file() 
            and GAME_MANIFEST_FILE_TYPE in entry.name
        )

    @staticmethod
    def get_launcher_manifest_files(launcher_manifests_path: str) -> list[FileDirectory]:
    
        launcher_manifest_file_list: list[FileDirectory] = []

        for manifest_entry in os.scandir(launcher_manifests_path):
            if GameDataManager.is_valid_launcher_manifest_file(manifest_entry):
                launcher_manifest_file_list.append(FileDirectory(manifest_entry.name, manifest_entry.path))
        
        return launcher_manifest_file_list
    
    @staticmethod
    def get_game_data_list(game_data_path: str):
    
        game_data_list: list[GameData] = []
        
        for game_entry in os.scandir(game_data_path):
            
            game_folder: FileDirectory = None
            manifest_folder: FileDirectory = None
            manifest_file_list: list[FileDirectory] = []

            if GameDataManager.is_valid_game_folder(game_entry) == False:
                print(f"WARNING!: Skipping \"{game_entry.name}/\" as it is not a valid game folder.")
                continue

            manifest_folder_path = os.path.join(game_entry.path, GAME_MANIFEST_FOLDER_NAME)

            for manifest_entry in os.scandir(manifest_folder_path):
                if GameDataManager.is_valid_game_manifest_file(manifest_entry):
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
    
    @staticmethod
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




    
import sys
import os

DEFAULT_MANIFESTS_PATH: str = "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests"

def assert_path_exists(path: str) -> None:
    if os.path.exists(path) == False:
        print("Error: Path does not exist!")
        exit(0)

def main():

    # Get epic games store manifests path ------------------------------------
   
    manifests_path: str = ""

    print("Default Manifests Path: ", DEFAULT_MANIFESTS_PATH)

    option: str = input("Use default manifests path? (y/n): ")
    if str.upper(option[0]) == 'N':
        manifests_path = input("Please input a valid path: ")
    else:
        manifests_path = DEFAULT_MANIFESTS_PATH

    assert_path_exists(manifests_path)

    # Get game data path ----------------------------------------------------
    
    # game_data_path: str = input("Please enter path containing all games: ")
    # assert_path_exists(game_data_path)

    # TODO - TEMP REMOVE LINE
    game_data_path = "E:\\Program Files\\Epic Games"

    # Get game list ----------------------------------------------------------

    game_path_list: list[str] = []

    for entry in os.scandir(game_data_path):
        game_path_list.append(entry.path)

    # Get manifest list ------------------------------------------------------

    manifest_filepath_list: list[str] = []

    for entry in os.scandir(manifests_path):
        if entry.is_file():
            manifest_filepath_list.append(entry.path)

    # Print results ----------------------------------------------------------

    print("Games Found: ", len(game_path_list))
    print("Manifest Files Found: ", len(manifest_filepath_list))

    # TODO - Need to check for config format version???

    # Get config value for detecting duplicates ------------------------------

    mandatory_folder_list: list[tuple[str, str]] = []

    for filepath in manifest_filepath_list:
        with open(filepath, "r") as manifest_file:
            while True:
                
                line = manifest_file.readline().rstrip()

                config_entry = line.split(":")
                if "MandatoryAppFolderName" in config_entry[0]:
                    mandatory_folder_list.append((config_entry[1][2:-2], filepath))
                    break
    
    # Put duplicates together for later removal ------------------------------

    duplicates_dict: dict[str, list[tuple[str, str]]] = {}

    for entry in mandatory_folder_list:
        if duplicates_dict.get(entry[0]) == None: # If name does not exist in the dict
            duplicates_dict[entry[0]] = [entry]
        else:
            duplicates_dict[entry[0]].append(entry)

    for list_entry in duplicates_dict.values():
        print("List_Entry: ", len(list_entry))

    # Find the most recent file in each duplicate list -----------------------

    most_recent_file_list = []

    for list_entry in duplicates_dict.values():
        if len(list_entry) > 1: # We know there are duplicates
            
            most_recent_file_index = -1
            most_recent_time = -1

            for i, entry in enumerate(list_entry):

                file_modified_time = os.stat(list_entry[i][1]).st_mtime_ns

                if file_modified_time > most_recent_time:
                    most_recent_time = file_modified_time
                    most_recent_file_index = i

            most_recent_file_list.append(list_entry[most_recent_file_index])

    print("Recent files")
    for entry in most_recent_file_list:
        print(entry[1])

# TODO - Scrap the removal of duplicates for now to another py file.
# Just make all duplicates linked to the same game if you have to

    











if __name__ == "__main__":
    main()

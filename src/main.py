import sys
from file_management import FileManagement
from game_data import GameDataManager
from menu_cli import MenuCLI


def main():

    launcher_manifest_folder: str = ""

    print("Welcome to Epic Games Relinker")
    print(f"INFO: Default Manifests Path: {GameDataManager.DEFAULT_MANIFESTS_PATH}")

    if MenuCLI.yes_no_prompt("Use default manifests path?"):
        launcher_manifest_folder = GameDataManager.DEFAULT_MANIFESTS_PATH
    else:
        launcher_manifest_folder = input("Please input a valid path: ")

    FileManagement.assert_path_exists(launcher_manifest_folder)

    games_folder: str = input("Please enter your games folder path: ")
    FileManagement.assert_path_exists(games_folder)

    game_data_manager = GameDataManager(launcher_manifest_folder, games_folder)

    if game_data_manager.get_game_count() == 0:
        print(f"ERROR!: No games found! Exiting...")
        sys.exit(1)

    menu_options = {
        "Backup Manifests",
        "Restore Manifests",
        "Move Game Installation",
        "Relink Manifests",
        "Exit"
    }

    choice = MenuCLI.numbered_prompt(header="Main Menu:", option_list=menu_options)

    match (choice):
        case 1:
            game_data_manager.backup_manifests()
        case 2:
            game_data_manager.restore_manifests()
        case 3:
            game_data_manager.move_game_installation()
        case 4:
            game_data_manager.relink_manifests()
        case 5:
            print("INFO: Exiting...")
            sys.exit(0)

    print("INFO: Process Complete! Exiting...")
    sys.exit(0)


if __name__ == "__main__":
    main()
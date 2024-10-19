# Epic Games Relinker
Used to relink and manage games from the Epic Games Launcher.

## Reason for the existence of this project:
- The launcher does not have the option to add preinstalled games to your library from a storage drive.
- The launcher does not have an option to move games. Moving a game manually will cause the launcher to be unable to locate the game.
- When a game is updated on another PC, the launcher either cannot locate the game or tries to update the game again.
- Official suggestions by Epic Games are workarounds.
  - [How to detect preinstalled game.](https://www.epicgames.com/help/en-US/c-Category_EpicGamesStore/c-EpicGamesStore_LauncherSupport/can-the-epic-games-launcher-detect-previously-installed-games-a000084800).
  - [How to move a game.](https://www.epicgames.com/help/en-US/c-Category_EpicGamesStore/c-EpicGamesStore_LauncherSupport/how-to-move-an-installed-game-from-the-epic-games-launcher-to-another-directory-on-your-computer-a000084687?sessionInvalidated=true)

## Features:
- Ability to relink preinstalled games to the launcher.
- Ability to move games to another folder location and stay linked to the launcher.
- Ability to backup game manifest files so that games can be brought over to another PC.
- Ability to restore game manifest files to the launcher.

## Requirements:
- Python 3

## How to use:

### How to relink games:
1. Run the `Backup Manifests` option.
2. Run the `Relink Manifests` option.
3. Run the `Restore Manifests` option.
4. The launcher should now recognize your preinstalled games.

Note: The `Relink Manifests` option will not work if the launcher does not have a manifest file already associated with the game. If you do not have access to the original launcher you installed the game from, you will need to follow the workaround provided by Epic Games in order to force the launcher to create a new manifest file.

### How to move games:
1. Run the `Backup Manifests` option.
2. Run the `Move Game Installation` option.
3. Run the `Restore Manifests` option.
4. The launcher will be able to recognize the games you have moved.

Note: Moving games manually through the file explorer will necessitate the relinking process in order for them to be rediscovered by the launcher.

### How to move games between PCs:
1. Run the `Backup Manifests` option.
2. Move your storage drive / games folder to another PC.
3. Run the `Restore Manifests` option.

## Research Notes:
- The current way in which the Epic Games Launcher works is that manifest files for games
exists within the program data directory for the launcher.
- These `.item` manifest files resides in `C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests` by default.
- The `.item` manifest file is a json dictionary which specifies the install location of the game,
version of the game, where game files and updates should be downloaded from, etc.
- Each `.item` manifest references an encoded `.manifest` file within the `.egstore/` folder for each game. Ex: `<games_folder>/<game_name>/.egstore/<file_name>.manifest`.
- The `.item` and `.manifest` files are originally created when a game is installed and will be updated by the launcher during game updates. 
- An issue arises because of the location of the `.item` manifest files. The file location is associated with the specific installation of the launcher, rather than with where a game's installation actually resides.
- If a game installation were to reside on an external storage drive, and the drive were to be moved to a secondary PC, the Epic Games launcher installed on that secondary PC would have no idea the games exist.
- This makes sense as the games residing on this drive have never been linked to this secondary launcher.
- However, the Epic Games launcher does not have a feature to link preinstalled games.
- Once each game is manually and individually linked via the method suggested by Epic Games, the secondary launcher will have an understanding of the location and version of the games.
- However, if we move the storage drive back to the primary PC, the launcher here will have an outdated `.item` manifest file associated with the game.
- Two different issues will arise:
1. If the secondary PC's launcher had updated the game. The primary PC launcher will still think the game is out of date, and attempt an update.
2. If the secondary PC's launcher had changed the name of the `.manifest` file associated with the game due to a game update, the primary PC will not be able to locate the game, as the primary launcher's `.item` manifest file is now dissociated with the `.manifest` file by name.
- As another topic, the Epic Games launcher does not feature a method to move a game installation to another folder.
- If a game were to be manually moved to another folder, the launcher would still have the original `.item` manifest file for the game, which specifies the original location for the game.
- Since the game no longer exists within the original folder location, the launcher will no longer list the game as installed.
- This is understandable.
- However, there is no user-friendly way to reassociate the game with the launcher, and a user will have to follow the workaround provided by Epic Games in order to manually and individually reassociate every game that has been moved.

## How can Epic Games fix this?
- The `.item` manifests that exist within the program data folder of the launcher should reside in the `.egstore/` folder for each game.
- The launcher should reference parent folders containing multiple games, rather than referencing each individual game. Ex: C:\Games\[Game_1\, Game_2\, Game_3\] where "Games" is the parent folder.
- The launcher should have a file within its program data directory, which specifies the locations of parent folders that have been linked by the user or created through the launcher.
- When installing a game, the user could pick from their existing parent folders, or choose to create another parent folder.
- When the launcher starts up, it would search through the parent folders to see which games are installed. The launcher would read the `.item` and `.manifest` files within the `.egstore/` folder for each game in order to understand the state of the game, as well as any information relating to the installation.

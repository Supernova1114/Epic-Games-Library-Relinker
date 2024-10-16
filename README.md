# Epic Games Relinker Project
Used to relink games to the Epic Games Store Launcher.

## Project Status:
- The `backup` and `restore` functions for launcher manifest files are functional.
- Other `move game` and `relink game` function are being developed.

## Goal:
- Make a system that allows for the relinking of games to the Epic Games Store Launcher.

## Issue:
- When a game is moved to another drive, launcher cannot locate the game.
- When game is updated on another PC, launcher either cannot find game or tries to update game again.
- Launcher does not have the option to add games to library from a storage drive.
- Official suggestions by Epic Games are [workarounds](https://www.epicgames.com/help/en-US/c-Category_EpicGamesStore/c-EpicGamesStore_LauncherSupport/can-the-epic-games-launcher-detect-previously-installed-games-a000084800). 

## Research Notes:
- The current way in which the Epic Games Launcher works is that a manifest file for a game
exists within a program data directory for the launcher. This file is of type `.item`
- This manifest file is a json dictionary which specifies the install location of the game,
version of the game, where game files and updates
should be downloaded from, etc.
- This manifest file is originally created when a game is downloaded and can be updated by the launcher
for game updates, etc. 
- This manifest file resides in C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests by default.
- The issue with the file residing in this location, is that the file specifies the version of the game.
If the game were to be updated by a secondary launcher, the secondary launcher would have an updated manifest that
contains the updated versioning of the game. However, the first launcher will have the outdated manifest file.
Therefore when the storage drive containing the games is reconnected to the first launcher, the launcher will
think that the games are out of date, which they are not.
- Another issue is that if a game were to be moved to a different file location, the manifest within the launcher
would not be updated as well. The manifest would contain the old location of the game data.
- Additionally, the launcher likes to regularly change the name of a game's manifest during updates, which as a consequence
will cause other launchers to lose track of the game's location as the other launchers will have an old manifest.

## How can Epic Games fix this?
- The game manifests that exist in the program data folder of each launcher does not need to reside in that location.
- A game manifest should reside in the .egstore/ of the specified game.
- The launcher should force a common parent folder for the installation of games. Such as "C:\...\Epic Games\".
Do not let the user put the game into C:\Users\Cameron\Documents when choosing a game install location for example.
This will let the launcher reference parent folders on separate storage drives containing many games, instead of having
to keep track of every individual game.
- The launcher will have a file within its program data directory, which specifies the locations of the parent folders containing multiple games.
- The user can either manually create a games folder and link this to the launcher, or the launcher can create this folder.
- When the launcher starts up, it will be able to look through the parent folders to see which games are installed. The launcher can look inside of the
manifests within the .egstore/ directory of each game as to find what state the game is in / find info relating to the game.
- The launcher needs a way to link a games folder with preinstalled games to the launcher.
- As games reside within a common games folder on each storage drive, if this common folder were to be moved, the user would just need to relink the parent
folder, rather than relink every individual game.
- The launcher needs a way to move games, rather than doing this manually and relinking the games. The launcher would have a list of parent game folders
in which the user can choose to move a game to. Or the user can create a new parent game folder, which would then show up in this list.

## How can we fix this?
- We cannot physically change what the launcher does.
- However, we can help the launcher discovering games and relink manifest files to the launcher. This will require a custom written program.
- The program will have the option to `backup` the game `.item` manifest files to a common directory such as `manifest_backups/` within a common games folder. (Or put these in the `.egstore/` folder for each game).
- The program will have the option to `restore` the `.item` manifest files to the program data directory of an Epic Games Launcher. The launcher will then be able to locate these games, and will have a reference to the proper version specification of the game.
- The program will have the option to `move` a game. The program will move the game install, and then update the location reference within the `.item` manifest associated with the game. The launcher will now be able to locate the game.
- The program will have the option to `relink` games. This will fix the broken file location references within manifest files of already existing games.

## Notes:
- It does not seem feasable to request a manifest for each game from the Epic servers programmatically.
So if there is a name and hash mismatch of the manifest file or a non-existant manifest file prior to the
use of the Epic-Games-Relinker program, the user will need to follow the manual workaround provided
by Epic Games. This will cause a new .egstore/ to be created for the game and a new `.item` manifest to be created.

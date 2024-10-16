# Epic Games Relinker Project
Used to relink games to the Epic Games Store Launcher.

## Project Status:
- Most of the functionality is not ready yet. (WIP)
- Backup and restore functions for launcher manifest files are working. You can find these under `src/`

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

## How can I fix this?
- We cannot physically change what the launcher does.
- However, we can help the launcher with discovering games.
- A custom program will need to be written.
- This program will have the option to backup the game `.item` manifest files to a common directory such as `manifest_backups/` within a common games folder. (Or put these in the `.egstore/` folder for each game).
- The program will have the option to restore these files in the program data directory of an Epic Games Launcher. The launcher will then be able to locate these games, and will have a reference to the proper version specification of the game.
- The program will have the option to move a game. The program will move the game install, and then update the `.item` manifests associated with the game to have the correct folder locations of the game. The launcher will now be able to locate the game.
The program will need to backup manifests, update the manifests, and then restore the manifests. The `manifest_backups/` folder as well as the launcher will now have the updated manifests.
- The program will have a relink games option. This will fix the broken file location references within manifest files of already existing games.

## Notes:
- It does not seem feasable to request a manifest for each game from the Epic servers programmatically.
So if there is a name and hash mismatch of the manifest file or a non-existant manifest file prior to the
use of the Epic-Games-Relinker program, the user will need to follow the manual workaround provided
by Epic.

## Design Plan:
- TODO - REREAD THIS.
- User will be able to specify a path to the Epic Launcher as well as a path to 
their currently installed games folder.
- User will use the "backup" function which copies currently linked launcher manifests 
to a "manifest_backup" folder which will reside on the same folder level as the 
root game folder. User will want to do this when they plan to use any games with 
another PC / Epic Launcher.
- When user is at an alternate PC, they use the "restore" function which copies
the manifests residing in the "manifest_backup" folder to the Epic Launcher manifest location.
If a manifest with the same hash name already exists, the user will need to choose whether or not
to proceed with an overwrite. (As the overwritten file may be some other game installation manifest).
This will most likely be extremely rare as the file names are hashes of some sort.
- Now that the alternate PC launcher has an up to date manifest file for the game, the launcher
will now be able to properly locate the game, as well as update the game if necessary.
- If the user decides that they want to move a game to a different folder location, they can use
the "move-installation" function. This function takes in a game name and a destination location.
The function will then move the game and the associated manifest.
- If the user wants to manually move the game, they can do so by copying the game to the new location,
and using the "relink-games" function. This function checks within the games folder. It will
check against the current installation location of the game, and the installation location
specified within the game's manifest file. It will then update the specified location value
if necessary.
- Once an installation is moved. The user can use the "restore" function to move the updated
manifest files into the Epic Launcher manifest directory, where the launcher will be able to then
use the files to lookup the locations of the games.
- The "manifest_backup" folder will have a file to keep track of information such as
the "last_backup_time" just for convenience.

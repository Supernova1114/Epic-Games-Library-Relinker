# Epic Games Relinker Project

## Goal:
- Make a system that allows for the relinking of games to the Epic Games Store.

## Issue:
- When a game is moved to another drive, Epic Launcher cannot find game.
- When game is updated on another PC, Epic Launcher cannot find game.
- Launcher does not have the ability to add games to known library from a drive.
- Official suggestions by Epic Games are [workarounds](https://www.epicgames.com/help/en-US/c-Category_EpicGamesStore/c-EpicGamesStore_LauncherSupport/can-the-epic-games-launcher-detect-previously-installed-games-a000084800). 
- The current way in which the Epic Games Launcher works is that on install,
a manifest file for the game will download. This manifest file is a json dictionary in
which specifies the install location, version of the game, where game files and updates
should be downloaded from, etc. 
- This manifest file resides in C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests
- Game installation locations also have their own manifest files that are linked to the launcher
manifest file.
- The issue with the file residing in this location, is that this file tells the launcher where
the game is installed, and what version it currently is.
- If the game is moved to another folder, there is a referential integrity issue. The launcher
reads the original manifest file, and sees that the game does not exist in the original location.
- The manifest file would need to be updated with the new directory in this case.
- If the game is updated on another computer. The launcher of that computer has the most recent
manifest file which states the correct version of the game. If we now move this game to the
original computer, the launcher looks for the game using an old manifest file.
- This is not only a problem due to a version mismatch, but the game installation location itself
has an updated manifest file, and so the launcher will be unable to discover the game as there
is a manifest file mismatch as well. 

## Notes:
- It does not seem feasable to request a manifest for each game from the Epic servers programmatically.
So if there is a mismatch of the manifest file or a non-existant manifest file prior to the
use of the Epic-Games-Relinker program, the user will need to follow the manual workaround provided
by Epic.

## Design Plan:
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
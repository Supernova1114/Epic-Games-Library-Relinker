from tkinter import filedialog, Tk

root_window: Tk = Tk()

root_window.geometry("400x400")

dialog = filedialog.askdirectory(initialdir="C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests", title="Select Launcher Manifest Directory")

print(dialog)

root_window.mainloop()
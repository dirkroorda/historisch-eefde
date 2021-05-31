import sys
import os
from shutil import rmtree, copy, copytree


def backup(backupDir, flatDir):
    print("Backup:")
    print(f"src    = {flatDir}")
    print(f"backup = {backupDir}")

    if os.path.exists(backupDir):
        rmtree(backupDir)

    copytree(flatDir, backupDir)


def getUpdates():
    modifications = {}
    nNew = 0
    nUpdated = 0
    nDeleted = 0
    total = 0

    with open("flickr.csv") as fh:
        next(fh)
        for line in fh:
            fields = line.rstrip("\n").split(",")
            name = fields[0].rsplit("/", 1)[1]
            if not name.endswith(".jpg"):
                continue
            total += 1
            new = fields[2]
            updated = fields[3]
            exif_updated = fields[5]
            deleted = fields[17]

            if new == "1":
                modifications[name] = "new"
                nNew += 1
            if new == "0" and (updated == "1" or exif_updated == "1"):
                modifications[name] = "updated"
                nUpdated += 1
            if deleted == "1":
                modifications[name] = "deleted"
                nDeleted += 1

    print(
        f"""
All photos: {total:>3}
New:        {nNew:>3}
Updated:    {nUpdated:>3}
Deleted:    {nDeleted:>3}
"""
    )
    return modifications


def placeUpdates(backupDir, flatDir, modifications):
    if not modifications:
        return
    todo = "todo"
    if os.path.exists(todo):
        rmtree(todo)
    os.mkdir(todo)

    for (mod, key) in sorted(modifications.items()):
        print(f"{key:<10}: {mod}")
        keyDir = "check" if key in {"deleted", "new"} else "replace"
        dstDir = f"todo/{keyDir}"
        modFile = f"{mod[0:-4]}!deleted.jpg" if key == "deleted" else mod
        if not os.path.exists(dstDir):
            os.mkdir(dstDir)

        src = f"{backupDir}/{mod}" if key == "deleted" else f"{flatDir}/{mod}"
        dst = f"{dstDir}/{modFile}"

        copy(src, dst)


def main(command, bu, flat):
    backupRoot = os.path.abspath(bu)
    backupDir = f"{backupRoot}/Flat"
    flatDir = os.path.abspath(flat)

    if command == "bu":
        backup(backupDir, flatDir)

    if command == "up":
        modifications = getUpdates()
        placeUpdates(backupDir, flatDir, modifications)


if __name__ == "__main__":
    main(*sys.argv[1:])

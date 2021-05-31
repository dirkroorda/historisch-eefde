import os
import sys
import yaml
from subprocess import run

import osxphotos

import flickrapi
import webbrowser
import pprint

pp = pprint.PrettyPrinter(indent=2)


COMMANDS = dict(
    flat="export compilation from Photos to flat directory in _local",
    dropbox="export compilation from Photos to hierarchical directory on Dropbox",
    toflickr="sync additions/deletions, metadata, albums with Flickr",
)
COMMAND_STR = "\n".join(f"{k:<10} : {v}" for (k, v) in sorted(COMMANDS.items()))


HELP = f"""
updatr «compilation» «command»

compilation: the name of a yaml file that describes a compilation

command:
{COMMAND_STR}

-h
--help
help  : print help and exit
"""


REPO_DIR = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}"
YAML_DIR = f"{REPO_DIR}/yaml"
TOML_DIR = f"{REPO_DIR}/toml"
LOCAL_DIR = f"{REPO_DIR}/_local"
FLICKR_CONFIG = f"{LOCAL_DIR}/flickr.yaml"
TOML_FILES = ("flat", "dropbox")
CONFIG_FILE = f"{YAML_DIR}/update.yaml"
WORK_DIR = f"{YAML_DIR}/works"

DROPBOX_DIR = os.path.expanduser("~/Dropbox")
# DROPBOX_DIR = f"{LOCAL_DIR}/Dropbox"


def console(*args, error=False):
    device = sys.stderr if error else sys.stdout
    device.write(" ".join(args) + "\n")
    device.flush()


def pretty(data):
    print(pp.pprint(data))


def readArgs():
    class A:
        pass

    A.work = None
    A.command = None

    args = sys.argv[1:]

    if not len(args) or args[0] in {"-h", "--help", "help"}:
        console(HELP)
        return None

    work = args[0]
    A.work = work
    args = args[1:]

    if not len(args):
        console(HELP)
        console("Missing command")
        return None

    if args[0] in {"-h", "--help", "help"}:
        console(HELP)
        return None

    command = args[0]
    args = args[1:]

    A.command = command

    if command not in COMMANDS:
        console(HELP)
        console(f"Wrong arguments: «{' '.join(args)}»")
        return None

    return A


def readYaml(path):
    with open(path) as fh:
        settings = yaml.load(fh, Loader=yaml.FullLoader)
    return settings


class Make:
    def __init__(self, work):
        class C:
            pass

        self.C = C
        self.work = work
        self.good = True

        if work:
            if not self.config():
                self.good = False

    def config(self):
        C = self.C
        work = self.work

        good = True

        c = dict(work=work)

        compConfig = f"{WORK_DIR}/{work}.yaml"
        if not os.path.exists(compConfig):
            console(f"No yaml file found for {work}: {compConfig}")
            return None

        with open(compConfig) as fh:
            settings = yaml.load(fh, Loader=yaml.FullLoader)
            for (k, v) in settings.items():
                if k == "skipKeywords":
                    c["skipTags"] = "|".join(f"/{s},|{s}/," for s in v)
                    v = set(v)
                elif k == "photoLib":
                    v = os.path.expanduser(v)
                c[k] = v

        c["dropboxDir"] = f"{LOCAL_DIR}/{work}/Dropbox"
        c["localDir"] = f"{LOCAL_DIR}/{work}"
        c["flatDir"] = f"{LOCAL_DIR}/{work}/Flat"
        c["albumDir"] = f"{LOCAL_DIR}/{work}/albums"
        c["tomlOutDir"] = f"{LOCAL_DIR}/{work}/toml"
        c["reportDir"] = f"{LOCAL_DIR}/{work}/csv"
        c["reportFlat"] = f"{LOCAL_DIR}/{work}/csv/flat.csv"
        c["reportDropbox"] = f"{LOCAL_DIR}/{work}/csv/dropbox.csv"
        c["tomlFlat"] = f"{LOCAL_DIR}/{work}/toml/flat.toml"
        c["tomlDropbox"] = f"{LOCAL_DIR}/{work}/toml/dropbox.toml"

        if not os.path.exists(FLICKR_CONFIG):
            console(f"No flickr config file found: {FLICKR_CONFIG}")
            return None
        with open(FLICKR_CONFIG) as fh:
            for (k, v) in yaml.load(fh, Loader=yaml.FullLoader).items():
                c[k] = v

        for (k, v) in c.items():
            setattr(C, k, v)

        for wd in (C.flatDir, C.tomlOutDir, C.reportDir, C.dropboxDir):
            if not os.path.exists(wd):
                os.makedirs(wd, exist_ok=True)

        for tomlFile in TOML_FILES:
            tomlInPath = f"{TOML_DIR}/{tomlFile}.toml"
            tomlOutPath = f"{LOCAL_DIR}/{work}/toml/{tomlFile}.toml"

            if not os.path.exists(tomlInPath):
                console(f"File not found: {tomlInPath}")
                good = None

            with open(tomlInPath) as fh:
                toml = fh.read()

            for k in ("albumName", "reportFlat", "skipTags"):
                toml = toml.replace(f"«{k}»", getattr(C, k, None))

            with open(tomlOutPath, "w") as fh:
                fh.write(toml)

        return good

    def doCommand(self, command):
        getattr(self, command)()

    def flat(self):
        C = self.C
        run(
            (
                f"osxphotos export"
                f" {C.photoLib} {C.flatDir}"
                f" --load-config {C.tomlFlat}"
            ),
            shell=True,
        )

    def dropbox(self):
        C = self.C
        run(
            (
                f"osxphotos export"
                f" {C.photoLib} {C.dropboxDir}"
                f" --load-config {C.tomlDropbox}"
            ),
            shell=True,
        )

    def meta(self):
        C = self.C
        photosdb = osxphotos.PhotosDB(dbfile=C.photoLib)
        photos = photosdb.photos(albums=[C.albumName])
        keywordSet = set()
        keywordsFromName = {}
        descriptionsFromName = {}
        self.keywordsFromName = keywordsFromName
        self.descriptionsFromName = descriptionsFromName

        for photoInfo in photos:
            fName = photoInfo.original_filename.removesuffix(".jpg")
            description = photoInfo.description
            keywords = photoInfo.keywords
            useKeywords = []
            for keyword in keywords:
                if keyword not in C.skipKeywords:
                    keywordSet.add(keyword.lower())
                    useKeywords.append(keyword)
            useKeywords.append(C.albumName)
            keywordsFromName[fName] = set(useKeywords)
            descriptionsFromName[fName] = description

        self.keywordList = [C.albumName.lower()] + sorted(keywordSet)

    def getPhotos(self, albumId):
        C = self.C
        flickr = self.flickr

        data = flickr.photosets.getPhotos(user_id=C.flickrUserId, photoset_id=albumId)[
            "photoset"
        ]
        nPages = data["pages"]
        albumPhotos = data["photo"]
        if nPages > 1:
            for p in range(2, nPages + 1):
                data = flickr.photosets.getPhotos(
                    user_id=C.flickrUserId, photoset_id=albumId, page=p
                )["photoset"]
                albumPhotos.extend(data["photo"])
        return albumPhotos

    def albums(self):
        C = self.C

        if not getattr(self, "keywordList", None):
            self.meta()
        keywordSet = set(self.keywordList)

        self.connectFlickr()
        flickr = self.flickr

        allAlbums = flickr.photosets.getList(user_id=C.flickrUserId)["photosets"][
            "photoset"
        ]
        idFromAlbum = {}
        albumFromId = {}
        albumsFromPhoto = {}
        photoFromId = {}
        idFromPhoto = {}
        self.photoFromId = photoFromId
        self.idFromPhoto = idFromPhoto
        self.idFromAlbum = idFromAlbum
        self.albumFromId = albumFromId
        self.albumsFromPhoto = albumsFromPhoto

        for album in allAlbums:
            albumTitle = album["title"]["_content"]
            if albumTitle.lower() not in keywordSet:
                continue
            albumId = album["id"]
            idFromAlbum[albumTitle] = albumId
            albumFromId[albumId] = albumTitle

        for (albumId, albumTitle) in albumFromId.items():
            albumPhotos = self.getPhotos(albumId)
            print(f"{albumTitle} {len(albumPhotos):>4} photos")

            for photo in albumPhotos:
                photoId = photo["id"]
                fileName = photo["title"]
                photoFromId[photoId] = fileName
                idFromPhoto[fileName] = photoId
                albumsFromPhoto.setdefault(fileName, set()).add(albumTitle)

        print(f"Total: {len(albumFromId):>4} albums on Flickr")
        print(f"Total: {len(photoFromId):>4} photos on Flickr")
        print(f"Total: {len(idFromPhoto):>4} titles on Flickr")

    def toflickr(self):
        if not getattr(self, "keywordList", None):
            self.meta()
        if not getattr(self, "albumFromId", None):
            self.albums()
        self.getUpdates()
        self.placeUpdates()
        self.adjustAlbums()

    def connectFlickr(self):
        C = self.C
        if not getattr(self, "flickr", None):
            flickr = flickrapi.FlickrAPI(
                C.flickrKey, C.flickrSecret, format="parsed-json"
            )

            if not flickr.token_valid(perms="write"):
                flickr.get_request_token(oauth_callback="oob")
                authorize_url = flickr.auth_url(perms="write")
                webbrowser.open_new_tab(authorize_url)
                verifier = str(input("Verifier code: "))
                flickr.get_access_token(verifier)
            self.flickr = flickr

    def getUpdates(self):
        C = self.C
        self.flat()

        modifications = {}
        self.modifications = modifications
        nNew = 0
        nUpdated = 0
        nDeleted = 0
        total = 0

        with open(C.reportFlat) as fh:
            next(fh)
            for line in fh:
                fields = line.rstrip("\n").split(",")
                name = fields[0].rsplit("/", 1)[1]
                if not name.endswith(".jpg"):
                    continue
                name = name.removesuffix(".jpg")
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

    def placeUpdates(self):
        modifications = self.modifications

        if not modifications:
            print("No metadata updates")
            return

        for (name, kind) in sorted(modifications.items()):
            if kind == "updated":
                self.replaceFlickr(name)
                print(f"REPLACED: {name}")

    def replaceFlickr(self, name):
        C = self.C
        flickr = self.flickr

        idFromPhoto = self.idFromPhoto
        descriptionsFromName = self.descriptionsFromName

        fileName = f"{C.flatDir}/{name}.jpg"
        photoId = idFromPhoto[name]
        with open(fileName, "rb") as fh:
            flickr.replace(fileName, photoId, fh, format="rest")
        description = descriptionsFromName[name]
        if description:
            flickr.photos.setMeta(photo_id=photoId, description=description)

    def adjustAlbums(self):
        flickr = self.flickr

        keywordsFromName = self.keywordsFromName
        albumsFromPhoto = self.albumsFromPhoto
        idFromPhoto = self.idFromPhoto
        idFromAlbum = self.idFromAlbum

        touchedAlbums = set()

        for (name, photoId) in idFromPhoto.items():
            keywords = keywordsFromName.get(name, set())
            albums = albumsFromPhoto.get(name, set())
            print(f"{name} {keywords=} {albums=}")
            for k in keywords:
                if k not in albums:
                    print(f"add {name} to album {k}")
                    albumId = idFromAlbum.get(k, None)
                    if albumId is None:
                        print(f"\tmake new album {k}")
                        albumId = self.makeAlbum(k, photoId)
                    else:
                        flickr.photosets.addPhoto(photoset_id=albumId, photo_id=photoId)
                    touchedAlbums.add(albumId)
            for a in albums:
                if a not in keywords:
                    print(f"remove {name} from album {k}")
                    albumId = idFromAlbum[a]
                    flickr.photosets.removePhoto(photoset_id=albumId, photo_id=photoId)

        for albumId in sorted(touchedAlbums):
            photos = flickr.photosets
            photos = ",".join(photo["id"] for photo in self.getPhotos(albumId))
            flickr.photosets.reorderPhotos(photoset_id=albumId, photo_ids=photos)

    def makeAlbum(self, name, photoId):
        flickr = self.flickr
        albumFromId = self.albumFromId
        idFromAlbum = self.idFromAlbum

        result = flickr.photosets.create(title=name, primary_photo_id=photoId)
        albumId = result["photoset"]["id"]
        albumFromId[albumId] = name
        idFromAlbum[name] = albumId
        return albumId


def main():
    A = readArgs()
    if A is None:
        return 0

    work = A.work
    command = A.command

    if not work:
        return

    Mk = Make(work)

    return Mk.doCommand(command)


if __name__ == "__main__":
    sys.exit(main())

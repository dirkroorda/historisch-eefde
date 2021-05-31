import flickrapi
import webbrowser
import pprint

pp = pprint.PrettyPrinter(indent=2)


def pretty(data):
    print(pp.pprint(data))


flickrKey = "f374358950540b1360f920b3a766697f"
flickrSecret = "309d7e31778b46f9"
userId = "128532317@N06"

flickr = flickrapi.FlickrAPI(flickrKey, flickrSecret, format="parsed-json")

if False:
    flickr.authenticate_via_browser(perms='write')

if True:
    print('Step 1: authenticate')

# Only do this if we don't have a valid token already
    if not flickr.token_valid(perms='write'):

        # Get a request token
        flickr.get_request_token(oauth_callback='oob')

        # Open a browser at the authentication URL. Do this however
        # you want, as long as the user visits that URL.
        authorize_url = flickr.auth_url(perms='write')
        webbrowser.open_new_tab(authorize_url)

        # Get the verifier code from the user. Do this however you
        # want, as long as the user gives the application the code.
        verifier = str(input('Verifier code: '))

        # Trade the request token for an access token
        flickr.get_access_token(verifier)

if False:
    data = flickr.photos.search(user_id="128532317@N06")["photos"]
    nPages = data["pages"]
    allPhotos = data["photo"]
    if nPages > 1:
        for p in range(2, nPages + 1):
            data = flickr.photos.search(user_id="128532317@N06", page=p)["photos"]
            allPhotos.extend(data["photo"])

    print(f"{len(allPhotos)} photos")

    for (i, photo) in enumerate(allPhotos):
        if photo["title"] == "1900-06-30T12-00-AABACA":
            print(f"PHOTO {i}")
            pretty(photo)

if True:
    thePhoto = {
        "farm": 66,
        "id": "51202688309",
        "isfamily": 0,
        "isfriend": 0,
        "ispublic": 1,
        "owner": "128532317@N06",
        "secret": "160d1b3317",
        "server": "65535",
        "title": "1900-06-30T12-00-AABACA",
    }

    fileName = "/Users/dirk/Dropbox/EenEeuwEefde/almenseweg/1900-06-30T12-00-CBBAA.jpg"
    with open(fileName, "rb") as fh:
        print(fileName)
        flickr.replace(fileName, "51202688309", fh, format="rest")

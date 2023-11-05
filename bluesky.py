import requests
import json
from datetime import datetime, timezone

BLUESKY_EMAIL = "example.bsky.social"
BLUESKY_PASSWORD = "123-456-789"
IMAGE_PATH = "./example.png"
IMAGE_MIMETYPE = "image/png"
IMAGE_ALT_TEXT = "brief alt text description of the image"

resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.server.createSession",
    json={"identifier": BLUESKY_HANDLE, "password": BLUESKY_APP_PASSWORD},
)
resp.raise_for_status()
session = resp.json()
print(session["accessJwt"])

# Fetch the current time
# Using a trailing "Z" is preferred over the "+00:00" format
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

# Required fields that each post must include
post = {
    "$type": "app.bsky.feed.post",
    "text": "Hello World!",
    "createdAt": now,
}

resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.repo.createRecord",
    headers={"Authorization": "Bearer " + session["accessJwt"]},
    json={
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": post,
    },
)
print(json.dumps(resp.json(), indent=2))
resp.raise_for_status()

with open(IMAGE_PATH, "rb") as f:
    img_bytes = f.read()

# this size limit is specified in the app.bsky.embed.images lexicon
if len(img_bytes) > 1000000:
    raise Exception(
        f"image file size too large. 1000000 bytes maximum, got: {len(img_bytes)}"
    )

# TODO: strip EXIF metadata here, if needed

resp = requests.post(
    "https://bsky.social/xrpc/com.atproto.repo.uploadBlob",
    headers={
        "Content-Type": IMAGE_MIMETYPE,
        "Authorization": "Bearer " + session["accessJwt"],
    },
    data=img_bytes,
)
resp.raise_for_status()
blob = resp.json()["blob"]

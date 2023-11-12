import os
import random
import cloudinary
import cloudinary.api
import cloudinary.uploader
import requests
from mastodon import Mastodon
from atproto import Client, models
from datetime import datetime
from urllib.parse import urlparse
import helpers
#import configLog

def login_to_bluesky(BLUESKY_EMAIL, BLUESKY_PASSWORD):
    print(f"BLUESKY_EMAIL: {BLUESKY_EMAIL}")
    #logger, _ = configLog.configure_logging()
    try:
        client = Client()
        client.login(BLUESKY_EMAIL, BLUESKY_PASSWORD)
        #logger.debug("Successfully logged in to Bluesky.")
    except Exception as e:
        print(f"1: Failed to log in to Bluesky: {e}")

def post_to_bluesky(BLUESKY_EMAIL, BLUESKY_PASSWORD, text, image_locations, alt_texts):
    #logger, _ = configLog.configure_logging()

    try:
        login_to_bluesky(BLUESKY_EMAIL, BLUESKY_PASSWORD)
    except Exception as e:
        print(f"2: Failed to log in to Bluesky: {e}")
        return False

    text = helpers.strip_html_tags(text)
    #logger.debug(f"Stripped text: {text}")

    images = []
    for idx, image_location in enumerate(image_locations):
        try:
            # Parse the URL and get the path
            url_parts = urlparse(image_location)
            local_file_path = url_parts.path[1:]  # Remove the leading '/'

            # Debug: log the current file path
            #logger.debug(f"Processing image file: {local_file_path}")

            # Open the image file from its location
            with open(local_file_path, 'rb') as img_file:
                img_data = img_file.read()

            upload = client.com.atproto.repo.upload_blob(img_data)
            images.append(models.AppBskyEmbedImages.Image(alt=alt_texts[idx], image=upload.blob))
            #logger.debug(f"Uploaded image: {upload.blob}")
        except Exception as e:
            # Exception handling: log the error and local file path
            #logger.exception(f"Unable to process the image file at {local_file_path} for Bluesky. Error: {e}")
            return False

    embed = models.AppBskyEmbedImages.Main(images=images) if images else None
    facets = helpers.generate_facets_from_links_in_text(text) if helpers.URL_PATTERN.search(text) else None
    #logger.debug(f"Embed: {embed}, Facets: {facets}")

    try:
        client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=client.me.did,
                collection='app.bsky.feed.post',
                record=models.AppBskyFeedPost.Main(
                    createdAt=datetime.now().isoformat(), text=text, embed=embed, facets=facets
                ),
            )
        )
        #logger.debug("Bluesky post created.")
    except Exception as e:
        #logger.exception(f"Failed to create Bluesky post: {e}")
        return False

    return True

def main():
    from os import environ

    CLOUDINARY_URL = environ['CLOUDINARY_URL']
    MASTODON_CLIENT_KEY = environ['MASTODON_CLIENT_KEY']
    MASTODON_CLIENT_SECRET = environ['MASTODON_CLIENT_SECRET']
    MASTODON_ACCESS_TOKEN = environ['MASTODON_ACCESS_TOKEN']
    MASTODON_BASE_URL = environ['MASTODON_BASE_URL']
    BLUESKY_EMAIL = environ['BLUESKY_EMAIL']
    BLUESKY_PASSWORD = environ['BLUESKY_PASSWORD']

    print(f"BLUESKY_EMAIL: {BLUESKY_EMAIL}")

    client = Client()
    client.login(BLUESKY_EMAIL, BLUESKY_PASSWORD)
    client.send_post(text='Hello World!')

    # ... The rest of your code remains unchanged ...

    # Mastodon authentication
    mastodon = Mastodon(
        client_id=MASTODON_CLIENT_KEY,
        client_secret=MASTODON_CLIENT_SECRET,
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    # Get image from Cloudinary
    out = cloudinary.api.resources(type="upload", max_results=500)
    length = len(out['resources'])
    upper = length - 1
    rando = random.randrange(0, upper)
    name = out['resources'][rando]['public_id']
    image = out['resources'][rando]['asset_id']
    txtname = 'image name: ' + str(name)
    print(txtname)

    # Generate AI model hashtag based on filename prefix
    ainame = txtname[12:15]
    if ainame == 'mj-':
        aihashtag = '#midjourney'
    elif ainame == 'sd-':
        aihashtag = '#StableDiffusion'
    else:
        aihashtag = ''
    print('AI model: ' + aihashtag)
    url = out['resources'][rando]['url']
    r = requests.get(url)

    # Retrieving data from the URL using get method
    with open(image, 'wb') as f:
        f.write(r.content)

    # Choose ship name from list
    rawname = random.choice(open('names.txt').readlines())
    shipname = rawname.rstrip()
    print('ship name: ' + shipname)

    # Create post text
    post = shipname + " does not exist #TerranTradeAuthority #AIArt " + aihashtag
    
    # post to Mastodon with image
    mastodon.media_post(image)
    mastodon.status_post(post, media_ids=[mastodon.media_post(image)['id']])

    # Post to Bluesky with text, image locations, and alt texts
    if not post_to_bluesky(BLUESKY_EMAIL, BLUESKY_PASSWORD, post, [image], [shipname]):
        print("3: Failed to post to Bluesky")

    # Delete image from Cloudinary
    cloudinary.uploader.destroy(name)

if __name__ == "__main__":
    main()

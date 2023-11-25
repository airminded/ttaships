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
#import helpers
#import configLog

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
    #client.send_post(text='Hello World!')

    # ... The rest of your code remains unchanged ...

    # Mastodon authentication
    mastodon = Mastodon(
        client_id=MASTODON_CLIENT_KEY,
        client_secret=MASTODON_CLIENT_SECRET,
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )

    # Bluesky authentication
    client = Client()
    client.login(BLUESKY_EMAIL, BLUESKY_PASSWORD)


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

    # Bluesky test
    with open(image, 'rb') as f:
        img_data = f.read()

    # Choose ship name from list
    rawname = random.choice(open('names.txt').readlines())
    shipname = rawname.rstrip()
    print('ship name: ' + shipname)

    # Create post text
    post = shipname + " does not exist #TerranTradeAuthority #AIArt " + aihashtag
    
    # post to Mastodon with image
    mastodon.media_post(image)
    mastodon.status_post(post, media_ids=[mastodon.media_post(image)['id']])

    # Post to Bluesky with image
    client.send_image(
            text=post, image=img_data, image_alt=''
        )

    # Delete image from Cloudinary
    cloudinary.uploader.destroy(name)

if __name__ == "__main__":
    main()

import os
import random
import cloudinary
import cloudinary.api
import cloudinary.uploader
import requests
from io import BytesIO
from mastodon import Mastodon
from atproto import Client, client_utils
from atproto_client.utils.text_builder import TextBuilder
from PIL import Image
from atproto_client import models

def main():
    from os import environ

    # Fetching environment variables
    CLOUDINARY_URL = environ['CLOUDINARY_URL']
    MASTODON_CLIENT_KEY = environ['MASTODON_CLIENT_KEY']
    MASTODON_CLIENT_SECRET = environ['MASTODON_CLIENT_SECRET']
    MASTODON_ACCESS_TOKEN = environ['MASTODON_ACCESS_TOKEN']
    MASTODON_BASE_URL = environ['MASTODON_BASE_URL']
    BLUESKY_EMAIL = environ['BLUESKY_EMAIL']
    BLUESKY_PASSWORD = environ['BLUESKY_PASSWORD']

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
    rando = random.randrange(0, length)
    resource = out['resources'][rando]
    name = resource['public_id']
    image = resource['asset_id']
    url = resource['url']

    # Download image from Cloudinary
    r = requests.get(url)
    with open(image, 'wb') as f:
        f.write(r.content)

    # Get image dimensions using Pillow
    with Image.open(image) as img:
        width, height = img.size
    print(f"Image dimensions: {width}x{height}")

    # Calculate aspect ratio
    aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(height=height, width=width)

    # Choose ship name from list
    with open('names.txt') as names_file:
        names = names_file.readlines()
        shipname = random.choice(names).rstrip()
    print('Ship name: ' + shipname)

    # Create post text
    post_mastodon = f"{shipname} does not exist #AIArt #midjourney"
    post_bluesky = f"{shipname} does not exist "

    # Post to Mastodon with image
    mastodon.media_post(image)
    mastodon.status_post(post_mastodon, media_ids=[mastodon.media_post(image)['id']])

    # Convert png to jpg for Bluesky
    with Image.open(image) as img:
        img_byte_array = BytesIO()
        img = img.convert('RGB')  # Convert to RGB before saving as JPG
        img.save(img_byte_array, format='JPEG')
        img_byte_array.seek(0)

    image_data = img_byte_array.getvalue()

    # Create a TextBuilder instance
    text_builder = TextBuilder()

    # Add text and tag to the builder
    text_builder.text(post_bluesky).tag('#AIArt','AIArt').text(' ').tag('#midjourney','midjourney')

    # Build the text and the facets
    post = text_builder.build_text()
    facets = text_builder.build_facets()

    # Post to Bluesky with image, aspect ratio, and specified facets
    client.send_image(
        text=post,
        image=image_data,
        image_alt='',
        image_aspect_ratio=aspect_ratio,
        facets=facets
    )

    # Delete image from Cloudinary
    cloudinary.uploader.destroy(name)

if __name__ == "__main__":
    main()

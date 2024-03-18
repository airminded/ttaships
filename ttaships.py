import os
import random
import cloudinary
import cloudinary.api
import cloudinary.uploader
import requests
import io
from mastodon import Mastodon
from atproto import Client, client_utils
from atproto_client.utils.text_builder import TextBuilder
from PIL import Image
from io import BytesIO

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
    with open('names.txt') as names_file:
        names = names_file.readlines()
        shipname = random.choice(names).rstrip()
    print('ship name: ' + shipname)

    # Create post text
    post = f"{shipname} does not exist #TerranTradeAuthority #AIArt {aihashtag}"
    
    # Post to Mastodon with image
    mastodon.media_post(image)
    mastodon.status_post(post, media_ids=[mastodon.media_post(image)['id']])

    # Convert png to jpg for Bluesky
    with Image.open(image) as img:
        img_byte_array = BytesIO()
        img = img.convert('RGB')  # Convert to RGB before saving as JPG
        img.save(img_byte_array, format='JPEG')
        img_byte_array.seek(0)  # Reset the pointer to the beginning of the byte array
    
    #processed_image = Image.open(img_byte_array)
    image_data = img_byte_array.getvalue()

    hashtag = 'AIArt'

    # Create a TextBuilder instance
    text_builder = TextBuilder()

    # Add text and tag to the builder
    text_builder.text('This is a rich message. ').tag('This is a tag.','atproto')

    # Build the text and the facets
    post = text_builder.build_text()
    facets = text_builder.build_facets()

    # Post to Bluesky with image and specified facets
    client.send_image(
        text=post,
        image=image_data,
        image_alt='',
        facets=facets  # Pass the list of facet objects here
    )
    
    # Create Tag facet object
    #tag_facet = Tag(tag=hashtag)  # Assuming the hashtag should be used as the tag value
    
    # Post to Bluesky with image
    #client.send_image(
    #        text=post, image=image_data, image_alt='', facets=[tag_facet]
   #     )

    # Delete image from Cloudinary
    #cloudinary.uploader.destroy(name)

if __name__ == "__main__":
    main()

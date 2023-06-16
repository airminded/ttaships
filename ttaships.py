import tweepy
import os
import random
import cloudinary
import cloudinary.api
import cloudinary.uploader
import requests
from mastodon import Mastodon

def main():
    from os import environ

    TWITTER_API_KEY = environ['TWITTER_API_KEY']
    TWITTER_API_SECRET = environ['TWITTER_API_SECRET']
    TWITTER_ACCESS_TOKEN = environ['TWITTER_ACCESS_TOKEN']
    TWITTER_ACCESS_TOKEN_SECRET = environ['TWITTER_ACCESS_TOKEN_SECRET']
    CLOUDINARY_URL = environ['CLOUDINARY_URL']
    MASTODON_CLIENT_KEY = environ['MASTODON_CLIENT_KEY']
    MASTODON_CLIENT_SECRET = environ['MASTODON_CLIENT_SECRET']
    MASTODON_ACCESS_TOKEN = environ['MASTODON_ACCESS_TOKEN']
    MASTODON_BASE_URL = environ['MASTODON_BASE_URL']

    # Twitter authentication
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    client = tweepy.Client( 
                       consumer_key='TWITTER_API_KEY', 
                       consumer_secret='TWITTER_API_SECRET', 
                       access_token='TWITTER_ACCESS_TOKEN', 
                       access_token_secret='TWITTER_ACCESS_TOKEN_SECRET')

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

    # Upload image to Twitter
    media = api.media_upload(filename=image)

    # Choose ship name from list
    rawname = random.choice(open('names.txt').readlines())
    shipname = rawname.rstrip()
    print('ship name: ' + shipname)

    # Create post text
    post = shipname + " does not exist #TerranTradeAuthority #AIArt " + aihashtag

    # Post to Twitter with image
    # tweet = api.update_status(status=post, media_ids=[media.media_id])
    # tweet = client.create_tweet(text=post, media_ids=[media.media_id], user_auth=True)
    
    # post to Mastodon with image
    mastodon.media_post(image)
    mastodon.status_post(post, media_ids=[mastodon.media_post(image)['id']])
    
    # Delete image from Cloudinary
    cloudinary.uploader.destroy(name)

if __name__ == "__main__":
    main()

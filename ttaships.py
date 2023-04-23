import tweepy
import os, random
import cloudinary,cloudinary.api,cloudinary.uploader
import requests
from mastodon import Mastodon

def main():

    from os import environ
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_KEY = environ['ACCESS_KEY']
    ACCESS_SECRET = environ['ACCESS_SECRET']
    CLOUDINARY_URL = environ['CLOUDINARY_URL']
    MASTODON_CLIENT_KEY = environ['MASTODON_CLIENT_KEY']
    MASTODON_CLIENT_SECRET = environ['MASTODON_CLIENT_SECRET']
    MASTODON_ACCESS_TOKEN = environ['MASTODON_ACCESS_TOKEN']
    MASTODON_BASE_URL = environ['MASTODON_BASE_URL']
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    mastodon = Mastodon(
        client_id=MASTODON_CLIENT_KEY,
        client_secret=MASTODON_CLIENT_SECRET,
        access_token=MASTODON_ACCESS_TOKEN,
        api_base_url=MASTODON_BASE_URL
    )
    
    # get image from cloudinary
    out = cloudinary.api.resources(type = "upload", max_results=500)
    length = len(out['resources'])
    upper=length-1
    rando = random.randrange(0,upper)
    name=out['resources'][rando]['public_id']
    image=out['resources'][rando]['asset_id']
    txtname = 'image name: ' + str(name)
    print(txtname)
    # generate AI model hashtag based on filename prefix
    ainame=txtname[12:15]
    if ainame == 'mj-':
        aihashtag = '#midjourney'
    elif ainame == 'sd-':
        aihashtag = '#StableDiffusion'
    else: 
        aihashtag = '#LookingGlassAI'
    print(aihashtag)
    url=out['resources'][rando]['url']
    r = requests.get(url)
    # retrieving data from the URL using get method
    with open(image, 'wb') as f:
        f.write(r.content)
    # delete image from cloudinary 
    cloudinary.uploader.destroy(name)

    # upload image to Twitter
    media = api.media_upload(image)

    # choose ship name from list
    rawname = random.choice(open('names.txt').readlines())
    name = rawname.rstrip()
 
    # post to Twitter with image
    tweet = name+" does not exist #TerranTradeAuthority #AIArt "+aihashtag
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])
    
    # post to Mastodon with image
    toot = name+" does not exist #TerranTradeAuthority #AIArt "+aihashtag
    mastodon.media_post(image)
    mastodon.status_post(toot, media_ids=[mastodon.media_post(image)['id']])

if __name__ == "__main__":
    main()

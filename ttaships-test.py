#https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/
import tweepy
import os, random
import cloudinary,cloudinary.api
import requests
 
def main():

# from credentials import *  # use this one for testing

    
# use this for production; set vars in heroku dashboard
#    consumer_key = environ['CONSUMER_KEY']
#    consumer_secret = environ['CONSUMER_SECRET']
#    access_key = environ['ACCESS_KEY']
#     access_secret = environ['ACCESS_SECRET']

    from os import environ
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_KEY = environ['ACCESS_KEY']
    ACCESS_SECRET = environ['ACCESS_SECRET']
    CLOUDINARY_URL = environ['CLOUDINARY_URL']



#    INTERVAL = 60 * 60 * 6  # tweet every 6 hours
    # INTERVAL = 15  # every 15 seconds, for testing

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
   
##    path = r"pics"
    path = "pics"
#    image = random.choice([
#        x for x in os.listdir(path)
#        if os.path.isfile(os.path.join(path, x))
#    ])
#    print(image)
    
    # get image from cloudinary
    out = cloudinary.api.resources(type = "upload")
    length = len(out['resources'])

    upper=length-1
    rando = random.randrange(0,upper)
    blah=out['resources'][rando]['public_id']
    image=out['resources'][rando]['asset_id']
    print(blah)
    url=out['resources'][rando]['url']
    print(url)
    r = requests.get(url)
    #retrieving data from the URL using get method
    with open(image, 'wb') as f:
        f.write(r.content) 
###    cloudinary.uploader.destroy(blah)


    # Upload image
    media = api.media_upload(image)
#    api.media_upload(image)
    api.media_upload(image)


    # Generate ship name
    rawname = random.choice(open('names.txt').readlines())
    name = rawname.rstrip()
 
    # Post tweet with image
#    tweet = "This TTA ship does not exist #LookingGlassAI"
    tweet = name+" does not exist #TerranTradeAuthority #LookingGlassAI"
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

#    os.remove(path+"/"+image) 

	
if __name__ == "__main__":
    main()

#https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/
import tweepy
import os, random
import cloudinary,cloudinary.api,cloudinary.uploader
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
   
    
    # get image from cloudinary
    # max_results = 500 is the max, otherwise defaults to 10
    out = cloudinary.api.resources(type = "upload", max_results=500)
    length = len(out['resources'])
    upper=length-1
    rando = random.randrange(0,upper)
    name=out['resources'][rando]['public_id']
    image=out['resources'][rando]['asset_id']
    txtname = 'image name: ' + str(name)
    print(txtname)
    ainame=txtname[12:15]
    print(ainame)
    print(ainame == 'mj-')
#    if ainame == 'mj-'
#        then aihashtag = '#midjourney'
#    elif ainame == 'da-'
#        then aihashtag = '#dalle2'
#    else aihashtag = '#LookingGlassAI'
#    print(aihashtag)
    url=out['resources'][rando]['url']
    r = requests.get(url)
    #retrieving data from the URL using get method
    with open(image, 'wb') as f:
        f.write(r.content) 
    cloudinary.uploader.destroy(name)

    # Upload image
    media = api.media_upload(image)
    api.media_upload(image)


    # Generate ship name
    rawname = random.choice(open('names.txt').readlines())
    name = rawname.rstrip()
 
    # Post tweet with image
#    tweet = "This TTA ship does not exist #LookingGlassAI"
    tweet = name+" does not exist #TerranTradeAuthority"
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

#    os.remove(path+"/"+image) 

	
if __name__ == "__main__":
    main()

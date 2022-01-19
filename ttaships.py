#https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/
import tweepy
import os, random
 
def main():

# from credentials import *  # use this one for testing
    twitter_auth_keys = {
        "consumer_key"        : "cQoQoUghaU1PO5NBf4UipF1J3",
        "consumer_secret"     : "0XW69g2a21aaQbBR2LxU4NhdcSo53hMAAltEk1aoCVdeiQofyq",
        "access_token"        : "1481148408664834049-anmMzMGywTkiPpDVgZHIXUZswBTvtl",
        "access_token_secret" : "x91Z6OrJu0bJcEHdhBhIfIdYKjs9k1uEdTv5V7ljrrA2r"
    }
    
# use this for production; set vars in heroku dashboard
#    consumer_key = environ['CONSUMER_KEY']
#    consumer_secret = environ['CONSUMER_SECRET']
#    access_key = environ['ACCESS_KEY']
#     access_secret = environ['ACCESS_SECRET']

##    from os import environ
##    twitter_auth_keys = {
##        "consumer_key"        : consumer_key = environ['CONSUMER_KEY'],
##        "consumer_secret"     : consumer_secret = environ['CONSUMER_SECRET'],
##        "access_token"        : access_key = environ['ACCESS_KEY'],
##        "access_token_secret" : access_secret = environ['ACCESS_SECRET']
##    }
 
    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)
   
#    path = r"pics"
    path = "pics"
    image = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    print(image)

    # Upload image
    media = api.media_upload(path+"/"+image)

 
    # Post tweet with image
    tweet = "This TTA ship does not exist"
    post_result = api.update_status(status=tweet, media_ids=[media.media_id])

    os.remove(path+"/"+image) 
	
if __name__ == "__main__":
    main()
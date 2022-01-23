#https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/
import tweepy
import os, random
 
def main():

    # Generate ship name
    raw = random.choice(open('names.txt').readlines())
    name = raw.rstrip()

    path = "pics2"
    image = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    print(image)
    os.remove(path+"/"+image)
 
    # Post tweet with image
#    tweet = "This TTA ship does not exist #LookingGlassAI"
    tweet = name+" #LookingGlassAI"

    print(tweet)
	
if __name__ == "__main__":
    main()

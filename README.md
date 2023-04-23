# ttaships
Twitter and Mastodon image bot

Original code base: https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/  

OAuth authentication used for both Twitter and Mastodon

This code: 
1. executes on Heroku
2. downloads a random image from Cloudinary
3. deletes that image from Cloudinary (i.e. so it won't be reposted)
4. creates a short post text (including a random phrase taken from names.txt) and a hashtag to specify the AI image generator used)
5. posts the text and image to Twitter
6. posts the same text and image to Mastodon

It can currently be seen in action at https://twitter.com/TTAships and https://sigmoid.social/@TTAships

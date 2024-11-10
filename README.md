# ttaships

## Mastodon and Bluesky image bot

Formerly a Twitter and Mastodon image bot, but Twitter is, well, you know

Original code base: https://www.mattcrampton.com/blog/step_by_step_tutorial_to_post_to_twitter_using_python_part_two-posting_with_photos/

This code: 
1. executes on Heroku
2. downloads a random image from Cloudinary
3. creates a short post text (including a random phrase taken from names.txt) and a hashtag to specify the AI image generator used, ~~based on the image filename prefix ("mj-" or "sd-")~~ (hashtags hardcoded as: #AIArt #midjourney)
4. posts the post text and PNG image to Mastodon
5. converts the PNG image to JPG (to shrink the file size, because Bluesky limits image file sizes to just under 1 MB)
6. posts the post text and JPG image to Bluesky
7. delete the image from Cloudinary (i.e. so it won't be reposted)

Note: there's currently no check for the filetype, PNG is assumed as that's what Midjourney creates

It can currently be seen in action on [@TTAships@sigmoid.social](https://sigmoid.social/@TTAships) and [@ttaships.airminded.org](https://bsky.app/profile/ttaships.airminded.org)

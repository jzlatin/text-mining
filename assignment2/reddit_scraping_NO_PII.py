import praw
import requests
import json

reddit = praw.Reddit(
    client_id=pass,
    client_secret=pass,
    password=pass,
    user_agent=pass,
    username=pass,
)
sub = 'HomeChef'
print(f'Subreddit: {sub}')

for post in reddit.subreddit(sub).top('month', limit=20):
    print(f'\n {post.title} \n\n')
    print(f'\n {post.selftext} \n\n')

sub = 'hellofresh'
print(f'Subreddit: {sub}')

for post in reddit.subreddit(sub).top('month', limit=20):
    print(f'\n {post.title} \n\n')
    print(f'\n {post.selftext} \n\n')

sub = 'blueapron'
print(f'Subreddit: {sub}')

for post in reddit.subreddit(sub).top('month', limit=20):
    print(f'\n {post.title} \n\n')
    print(f'\n {post.selftext} \n\n')

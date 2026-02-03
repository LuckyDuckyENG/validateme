import praw
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Reddit client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

# Test search in r/SaaS
print("Testing Reddit API...")
print("\nSearching r/SaaS for 'validation':\n")

for submission in reddit.subreddit("SaaS").search("validation", time_filter="month", limit=10):
    print(f"Title: {submission.title}")
    print(f"Author: u/{submission.author}")
    print(f"Score: {submission.score}")
    print(f"URL: https://reddit.com{submission.permalink}")
    print("-" * 80)

print("\n✅ Reddit API working!")

import praw
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

def search_reddit(keywords, subreddits=["SaaS", "startups", "Entrepreneur"], limit=20):
    """
    Search multiple subreddits for posts containing keywords
    Returns list of dicts with post data
    """
    results = []

    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)

            for submission in subreddit.search(keywords, time_filter="month", limit=limit):
                # Get post snippet (first 200 chars of selftext)
                snippet = submission.selftext[:200] + "..." if len(submission.selftext) > 200 else submission.selftext

                post_data = {
                    'username': str(submission.author),
                    'title': submission.title,
                    'snippet': snippet,
                    'subreddit': subreddit_name,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d'),
                    'url': f"https://reddit.com{submission.permalink}"
                }

                results.append(post_data)
        except Exception as e:
            print(f"Error searching r/{subreddit_name}: {e}")
            continue

    # Sort by score (engagement)
    results.sort(key=lambda x: x['score'], reverse=True)

    return results[:20]  # Return top 20

# Test
if __name__ == "__main__":
    results = search_reddit("validation")
    print(f"Found {len(results)} posts\n")

    for post in results[:5]:
        print(f"u/{post['username']} - {post['title']}")
        print(f"r/{post['subreddit']} | {post['score']} upvotes | {post['created_utc']}")
        print(f"{post['snippet']}\n")

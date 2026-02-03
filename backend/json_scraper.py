import requests
from datetime import datetime
import time

def search_reddit_json(keywords, subreddits=["SaaS", "startups", "Entrepreneur"], limit=20):
    """
    Search Reddit using the public JSON API (no authentication required)
    """
    results = []
    headers = {'User-Agent': 'ValidateMe/1.0'}

    for subreddit_name in subreddits:
        try:
            # Search using Reddit's JSON endpoint
            url = f"https://www.reddit.com/r/{subreddit_name}/search.json"
            params = {
                'q': keywords,
                't': 'month',  # time filter: month
                'limit': limit,
                'restrict_sr': 'on',  # restrict to this subreddit
                'sort': 'top'
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])

                for post in posts:
                    post_data = post.get('data', {})

                    # Get post snippet (first 200 chars)
                    selftext = post_data.get('selftext', '')
                    snippet = selftext[:200] + "..." if len(selftext) > 200 else selftext

                    result = {
                        'username': post_data.get('author', '[deleted]'),
                        'title': post_data.get('title', ''),
                        'snippet': snippet,
                        'subreddit': subreddit_name,
                        'score': post_data.get('score', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'created_utc': datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d'),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}"
                    }

                    results.append(result)
            else:
                print(f"Error searching r/{subreddit_name}: HTTP {response.status_code}")

            # Be nice to Reddit - add delay between requests
            time.sleep(1)

        except Exception as e:
            print(f"Error searching r/{subreddit_name}: {e}")
            continue

    # Sort by score (engagement)
    results.sort(key=lambda x: x['score'], reverse=True)

    return results[:20]  # Return top 20

# Test
if __name__ == "__main__":
    results = search_reddit_json("validation")
    print(f"Found {len(results)} posts\n")

    for post in results[:5]:
        print(f"u/{post['username']} - {post['title']}")
        print(f"r/{post['subreddit']} | {post['score']} upvotes | {post['created_utc']}")
        print(f"{post['snippet']}\n")

# ValidateMe - Setup Guide

## Project Overview
ValidateMe: Find people to validate your startup idea with (no audience required).

**Core functionality:**
- Input: Startup problem/idea
- Output: 10-20 Reddit posts from people mentioning the pain + personalized DM templates

---

## Day 1: Project Setup + Reddit API

### 1. Create project structure
```bash
mkdir validateme
cd validateme

# Create folders
mkdir backend
mkdir frontend
mkdir static
mkdir templates
```

### 2. Set up Python environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install praw openai flask python-dotenv
pip freeze > requirements.txt
```

### 3. Get Reddit API credentials

1. Go to: https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in:
   - **Name:** validateme
   - **App type:** script
   - **Description:** Find people to validate your startup idea with
   - **About URL:** (leave blank)
   - **Redirect URI:** http://localhost:8080
4. Click "Create app"
5. Save:
   - **client_id** (under "personal use script")
   - **client_secret** (next to "secret")

### 4. Create `.env` file
```bash
# Create .env in project root
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USER_AGENT=validateme-v1
OPENAI_API_KEY=your_openai_key_here
```

### 5. Test basic Reddit scraping

Create `backend/test_reddit.py`:

```python
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
```

Run test:
```bash
python backend/test_reddit.py
```

**Success criteria:** You see 10 posts about validation from r/SaaS

---

## Day 2: Core scraping logic

Create `backend/scraper.py`:

```python
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
```

---

## Day 3: AI DM template generation

Create `backend/ai_templates.py`:

```python
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_dm_templates(username, post_title, post_snippet):
    """
    Generate 3 personalized DM templates based on post content
    """

    prompt = f"""
    A Reddit user u/{username} posted:

    Title: {post_title}
    Content: {post_snippet}

    Generate 3 short, personalized DM templates (2-3 sentences each) to reach out to them.

    Requirements:
    - Acknowledge their specific struggle
    - Ask a genuine question (not pitching anything)
    - Peer-to-peer tone (not salesy)
    - Keep it under 50 words each

    Format as:
    Template 1:
    [message]

    Template 2:
    [message]

    Template 3:
    [message]
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content

# Test
if __name__ == "__main__":
    test_username = "ponziedd"
    test_title = "How long should I spend validating?"
    test_snippet = "I launched an app 2.5 weeks ago and got no beta signups..."

    templates = generate_dm_templates(test_username, test_title, test_snippet)
    print(templates)
```

---

## Day 4-5: Flask backend + simple frontend

Create `backend/app.py`:

```python
from flask import Flask, render_template, request, jsonify
from scraper import search_reddit
from ai_templates import generate_dm_templates

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    keywords = data.get('keywords', '')

    # Search Reddit
    results = search_reddit(keywords)

    # Generate DM templates for each result
    for result in results:
        result['dm_templates'] = generate_dm_templates(
            result['username'],
            result['title'],
            result['snippet']
        )

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

Create `templates/index.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>ValidateMe</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        input { width: 100%; padding: 10px; font-size: 16px; margin-bottom: 10px; }
        button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { border: 1px solid #ddd; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .username { color: #007bff; font-weight: bold; }
        .template { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 3px; }
        .copy-btn { background: #28a745; color: white; border: none; padding: 5px 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Find People to Validate With</h1>
    <input type="text" id="keywords" placeholder="What problem are you solving? (e.g., 'founders struggling with validation')">
    <button onclick="search()">Find People</button>

    <div id="results"></div>

    <script>
        async function search() {
            const keywords = document.getElementById('keywords').value;
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<p>Searching...</p>';

            const response = await fetch('/search', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({keywords})
            });

            const data = await response.json();

            resultsDiv.innerHTML = '';
            data.results.forEach(result => {
                resultsDiv.innerHTML += `
                    <div class="result">
                        <div class="username">u/${result.username}</div>
                        <strong>${result.title}</strong>
                        <p>${result.snippet}</p>
                        <small>r/${result.subreddit} | ${result.score} upvotes | ${result.created_utc}</small>

                        <h4>DM Templates:</h4>
                        <div class="template">
                            ${result.dm_templates.replace(/\n/g, '<br>')}
                            <br><button class="copy-btn" onclick="copyToClipboard(this)">Copy</button>
                        </div>
                    </div>
                `;
            });
        }

        function copyToClipboard(btn) {
            const text = btn.parentElement.innerText.replace('Copy', '').trim();
            navigator.clipboard.writeText(text);
            btn.innerText = 'Copied!';
            setTimeout(() => btn.innerText = 'Copy', 2000);
        }
    </script>
</body>
</html>
```

---

## Running the app

```bash
# Activate venv
venv\Scripts\activate

# Run Flask
python backend/app.py

# Open browser
http://localhost:5000
```

---

## Success Criteria

**Day 1:** Reddit API works, can scrape posts ✅
**Day 2:** Can search multiple subreddits + filter results ✅
**Day 3:** AI generates personalized DM templates ✅
**Day 4-5:** Full UI works (input → results → copy DMs) ✅
**Day 6:** YOU use it to validate your next idea ✅
**Day 7:** 2-3 other founders test it ✅

---

## Next Steps (Week 2)

- Add tracking (who you DMed, responses)
- Add Twitter scraping
- Simple pricing page
- Deploy (Heroku/Railway)

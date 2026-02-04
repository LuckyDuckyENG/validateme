from flask import Flask, render_template, request, jsonify
from backend.json_scraper import search_reddit_json
from backend.ai_templates import generate_dm_templates
import sys

# Force stdout to flush immediately (so logs show up in Render)
sys.stdout.flush()

print("Using Reddit JSON API (no authentication required)", flush=True)

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    keywords = data.get('keywords', '')

    print(f"🔍 SEARCH REQUEST: '{keywords}'", flush=True)  # Log the search

    # Search Reddit using JSON API (no auth required)
    results = search_reddit_json(keywords)

    print(f"✅ SEARCH COMPLETE: Found {len(results)} results for '{keywords}'", flush=True)

    # Don't generate AI templates yet - return results immediately
    return jsonify({'results': results})

@app.route('/generate-dm', methods=['POST'])
def generate_dm():
    data = request.json
    username = data.get('username', '')
    title = data.get('title', '')
    snippet = data.get('snippet', '')

    print(f"🤖 DM GENERATION REQUEST for u/{username}", flush=True)

    # Generate DM templates for this specific post
    templates = generate_dm_templates(username, title, snippet)

    print(f"✅ DM TEMPLATES GENERATED for u/{username}", flush=True)

    return jsonify({'dm_templates': templates})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

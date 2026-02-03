from flask import Flask, render_template, request, jsonify
from json_scraper import search_reddit_json
from ai_templates import generate_dm_templates

print("Using Reddit JSON API (no authentication required)")

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    keywords = data.get('keywords', '')

    # Search Reddit using JSON API (no auth required)
    results = search_reddit_json(keywords)

    # Don't generate AI templates yet - return results immediately
    return jsonify({'results': results})

@app.route('/generate-dm', methods=['POST'])
def generate_dm():
    data = request.json
    username = data.get('username', '')
    title = data.get('title', '')
    snippet = data.get('snippet', '')

    # Generate DM templates for this specific post
    templates = generate_dm_templates(username, title, snippet)

    return jsonify({'dm_templates': templates})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

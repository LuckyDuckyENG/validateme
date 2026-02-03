from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_dm_templates(username, post_title, post_snippet):
    """
    Generate 3 personalized DM templates based on post content
    """

    prompt = f"""You are helping someone reach out to a Reddit user who posted about their struggles. Write 3 different personalized DM templates.

Reddit Post:
- Username: u/{username}
- Title: {post_title}
- Content: {post_snippet}

Write 3 short DM templates (2-3 sentences each) that:
- Reference SPECIFIC details from their post (don't use placeholders like [Name] or [struggle])
- Sound like a peer reaching out, not a salesperson
- Ask a genuine curious question about their situation
- Are conversational and friendly
- Start naturally (Hi, Hey, or just jump in)
- Keep under 50 words each

DO NOT use placeholders. Use actual details from the post.

Format:
Template 1:
[your message here]

Template 2:
[your message here]

Template 3:
[your message here]"""

    response = client.chat.completions.create(
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

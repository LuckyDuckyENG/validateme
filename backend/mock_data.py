"""
Mock Reddit data for testing without API credentials
"""

def get_mock_results(keywords):
    """
    Returns mock Reddit posts for testing
    """
    return [
        {
            'username': 'startup_founder_23',
            'title': 'Struggling to validate my SaaS idea - how do I find early users?',
            'snippet': 'I have been working on a project management tool for remote teams but I am having trouble finding people to validate it with. I do not have an audience yet and cold outreach is not working...',
            'subreddit': 'SaaS',
            'score': 47,
            'num_comments': 23,
            'created_utc': '2026-01-28',
            'url': 'https://reddit.com/r/SaaS/mock1'
        },
        {
            'username': 'indie_dev_2024',
            'title': 'Built an MVP but got zero sign-ups. What am I doing wrong?',
            'snippet': 'Spent 3 months building my app, launched it last week on Product Hunt and got 200 upvotes but literally zero beta sign-ups. Is my idea just bad? Should I pivot or keep going?',
            'subreddit': 'startups',
            'score': 112,
            'num_comments': 67,
            'created_utc': '2026-01-25',
            'url': 'https://reddit.com/r/startups/mock2'
        },
        {
            'username': 'ponziedd',
            'title': 'How long should I spend validating my startup idea?',
            'snippet': 'I launched an app 2.5 weeks ago and got no beta signups. Should I keep trying to validate or just move on? How do you know when to quit vs when to persevere?',
            'subreddit': 'Entrepreneur',
            'score': 89,
            'num_comments': 45,
            'created_utc': '2026-01-22',
            'url': 'https://reddit.com/r/Entrepreneur/mock3'
        },
        {
            'username': 'tech_founder_99',
            'title': 'Need advice: No audience, no users, how to validate?',
            'snippet': 'I am a solo technical founder with an idea for a B2B tool. Problem is I have zero followers, no email list, no Twitter presence. How do people validate ideas when starting from scratch?',
            'subreddit': 'SaaS',
            'score': 156,
            'num_comments': 92,
            'created_utc': '2026-01-20',
            'url': 'https://reddit.com/r/SaaS/mock4'
        },
        {
            'username': 'confused_builder',
            'title': 'Validation feels impossible - am I approaching this wrong?',
            'snippet': 'Every article says to validate before building, but how do you validate when nobody wants to talk to you? I have tried posting in communities, DMing people, nothing works. What am I missing?',
            'subreddit': 'startups',
            'score': 203,
            'num_comments': 134,
            'created_utc': '2026-01-18',
            'url': 'https://reddit.com/r/startups/mock5'
        }
    ]

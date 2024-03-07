from flask import Flask, jsonify
import requests
import re

app = Flask(_name_)

def get_latest_stories():
    url = "https://time.com"
    response = requests.get(url)
    if response.status_code == 200:
        # Extracting the response content from response
        html_content = response.text

        # Defining the regex patterns for content and associated link
        pattern = r'<li class="latest-stories_item">\s*<a href="([^"]+)">\s*<h3 class="latest-stories_item-headline">(.*?)</h3>'

        # Finding all matched of the specified patterns
        matches = re.findall(pattern, html_content)

        # Extract the latest 6 stories
        latest_stories = []
        for i in range(min(len(matches),  6)):
            link  = matches[i][0]
            content = matches[i][1]
            if link.startswith('/'):
                link = url + link
            latest_stories.append({'title':content.strip(), 'link': link})
        
        return latest_stories
    else:
        print("Failed to load Time.com's homepage.")
        return None

@app.route('/getTimeStories')
def get_time_stories():
    latest_stories = get_latest_stories()
    if latest_stories:
        return jsonify(latest_stories)
    else:
        return jsonify({'error': 'Failed to load Time.com\'s homepage.'}), 500

if _name_ == "_main_":
    app.run(debug=True)
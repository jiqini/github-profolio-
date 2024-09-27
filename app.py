import os
from flask import Flask, render_template, request, jsonify
from newsapi import NewsApiClient
import requests
from openai import OpenAI
from dotenv import load_dotenv
import datetime

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Get API keys from environment variables
openai_api = os.getenv('OPENAI_API_KEY')
news_api = os.getenv('NEWS_API_KEY')

client = OpenAI(api_key=openai_api)

# Initialize the News API client
nfl_news_api = NewsApiClient(api_key=news_api)

# tells what url for flask to trigger a specific function
@app.route('/')
def root():
    return render_template('index.html')

# if the user does not ask question relevant to fantasy football
def get_ai_response(user_msg):
    try:
        # Call the OpenAI API to get a response
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_msg}])

        # Extract the reply from the response
        reply = response.choices[0].message.content

        return jsonify({"response": reply})

    except Exception as e:
        # Handle errors gracefully
        print(f"Error from OpenAI API: {str(e)}")  # Debugging statemen
        return jsonify({"error": str(e)}), 500

#def fetch_nfl_news_for_player(player_name):
    #print(f"Fetching news for player: {player_name}")  # Debug print
    #news_response = fetch_nfl_news()
    
    #print("Response from fetch_nfl_news:", news_response)
    #print("Response type:", type(news_response))
    #print("Response content:", news_response.get_json() if hasattr(news_response, 'get_json') else news_response)

    return news_response

@app.route('/get_nfl_news')
def fetch_nfl_news_for_player(player_name):
    player_name = request.args.get('player')
    print(f"Received player name: {player_name}") 
    if not player_name:
        return jsonify({"error": "No player name provided"}), 400

    try:
        news_response = nfl_news_api.get_everything(
            q=player_name,
            language='en',
            sort_by='publishedAt',
        )
        print("News API Response:", news_response)  # Debugging statement

        articles = news_response.get('articles', [])
        if not articles:
            return jsonify({"response": f"No relevant news found for {player_name}."}), 200

        # Sort articles by published date (most recent first)
        sorted_articles = sorted(articles, key=lambda x: x['publishedAt'], reverse=True)
        
        # Select the top 3 most recent articles
        top_articles = sorted_articles[:3]

        formatted_news = f"Recent news about {player_name}:\n\n"
        for article in sorted_articles:
            published_date = datetime.datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = published_date.strftime("%B %d, %Y")
            formatted_news += f"• {article['title']}\n"
            formatted_news += f"  Published on {formatted_date}\n"
            formatted_news += f"  Read more: {article['url']}\n\n"
        
        return jsonify({"response": formatted_news})

    except Exception as e:
        print(f"Error in fetch_nfl_news: {str(e)}")  # Debugging statement
        return jsonify({"error": str(e)}), 500


@app.route('/get_user')
def get_user_details(username):
    # Extract the username from the URL/query parameter
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "No username provided"}), 400

    # Construct the URL for the Sleeper API request through username, league id
    username_url = f"https://api.sleeper.app/v1/user/{username}"

    try:
        print(f"Requesting data from: {username_url}")  # Debugging statement

        user_response = requests.get(username_url)
        # Raise an error if the request failed
        user_response.raise_for_status()
        # converts the JSON response from the API into a Python dictionary
        user_data = user_response.json()

        print("Received data:", user_data)  # Debugging statement

        # Extract relevant user information
        user_info = {
            "username": user_data.get("username"),
            "display_name": user_data.get("display_name"),
            "avatar": user_data.get("avatar")
        }
        # Return the user details as JSON
        return jsonify(user_info)

    except requests.RequestException as e:
        print(f"Request failed: {e}")  # Debugging statement
        # Handle any errors that occur during the API request
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Debugging statement
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/get_league')
def get_league_details(league_id):
    league = request.args.get('leagueId')
    if not league:
        return jsonify({"error": "No league ID provided"}), 400

    league_url = f"https://api.sleeper.app/v1/league/{league}"

    try:
        league_response = requests.get(league_url)
        league_response.raise_for_status()
        # Convert the JSON response from the API into a Python dictionary
        league_data = league_response.json()

        return jsonify(league_data)
    except requests.RequestException as e:
        # Handle any errors that occur during the API request
        print(f"Request failed: {e}")  # Debugging statement
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        # Handle any unexpected errors
        print(f"An unexpected error occurred: {e}")  # Debugging statement
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/get_roster')
def get_roster():
    league_id = request.args.get('leagueId')

    if not league_id:
        return jsonify({"error": "No league ID provided"}), 400

    # Construct the URL for the Sleeper API request using the league ID
    roster_url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"

    try:
        print(f"Requesting data from: {roster_url}")  # Debugging statement

        response = requests.get(roster_url)
        response.raise_for_status()
        roster_data = response.json()

        print("Received data:", roster_data)  # Debugging statement

        return jsonify(roster_data)

    except requests.RequestException as e:
        print(f"Request failed: {e}")  # Debugging statement
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Debugging statement
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/chatbot')
def chatBot():
    return chat_bot()

def chat_bot():
    user_msg = request.args.get('message')
    try:
        # Check if the message is asking for news
        if "news about" in user_msg.lower():
            player_name = user_msg.split("news about")[-1].strip()
            if not player_name:
                return jsonify({"error": "Player name not provided"}), 400

            # Fetch NFL news for the specified player
            return fetch_nfl_news_for_player(player_name)

        # Check if the message is asking for user details
        elif "user" in user_msg.lower():
            username = user_msg.split("user")[-1].strip()
            return get_user_details(username)

        # Check if the message is asking for league details
        elif "league" in user_msg.lower():
            league_id = user_msg.split("league")[-1].strip()
            return get_league_details(league_id)

        # For all other messages, get AI response
        else:
            return get_ai_response(user_msg)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    # 'debug=True' flag; if error flask will show them in your browser
    app.run(debug=True)


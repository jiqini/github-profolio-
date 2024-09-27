# Fantasy Football Chatbot

## Project Description

The Fantasy Football Chatbot is an interactive tool designed to assist fantasy football enthusiasts in making informed decisions about their team management. This chatbot helps users with:

- Start/Sit decisions for their fantasy football lineup
- Providing the most relevant and up-to-date news articles about specific players
- Keeping users informed about injuries, press conference updates, and other crucial information

By leveraging natural language processing and real-time data fetching, this chatbot aims to give fantasy football players a competitive edge in their leagues.

## Technologies Used

- Python: The core programming language used for backend development
- Flask: Web framework for creating the API endpoints
- OpenAI API: For natural language processing and generating chatbot responses
- NewsAPI: To fetch the latest news articles about players
- Sleeper API: To retrieve fantasy football league and player data

## Features

- Interactive chat interface for user queries
- Player-specific news retrieval
- Start/Sit recommendations based on player statistics and matchups
- Integration with fantasy football league data

## Installation and Setup

1. Clone the repository:
    - git clone https://github.com/yourusername/fantasy-football-chatbot.git

2. Navigate to the project directory:
    - e.g. cd fantasy-football-chatbot

3. Install required dependencies:
    - pip install -r requirements.txt

4. Set up environment variables:
    - OPENAI_API_KEY=your_openai_api_key (you can get this from searching "openai api")
    - NEWS_API_KEY=your_news_api_key

5. Run the application:
    - python app.py

6. Open your web browser and go to `http://localhost:5000` to start using the chatbot.

## How to Use

1. Type your fantasy football related questions into the chat interface.
2. For player news, use the format: "news about [player name]"
3. For start/sit advice, ask something like: "Should I start [Player A] or [Player B] this week?"
4. The chatbot will provide responses based on the latest data and news available.

## Future Enhancements

- Deploy and scale the application on AWS for improved performance and reliability
- Implement machine learning models for more accurate start/sit predictions
- Add support for multiple fantasy football platforms like espn, yahoo! sports, etc.

## Credits

This project was developed by Ji Qi Ni and uses the following APIs:
- OpenAI API
- NewsAPI
- Sleeper API
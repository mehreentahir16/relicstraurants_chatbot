# Relicstraunts Chatbot

Relicstraunts is a customer service chatbot that assists users in finding restaurants, viewing menus, and getting recommendations. The bot is built using Flask and OpenAI’s GPT-4o model and integrates with New Relic to monitor performance metrics and optimize AI-driven responses.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Monitoring with New Relic](#monitoring-with-new-relic)

## Features

- Provides restaurant recommendations based on user queries
- Retrieves menus and detailed restaurant information
- Tracks key performance metrics using New Relic AI Monitoring

## Requirements

Before you begin, ensure you have met the following requirements:

- **Python 3.8+**
- **OpenAI API Key**: [Sign up or log in to OpenAI](https://beta.openai.com/signup/) to retrieve your API key.
- **New Relic account**: [Sign up for free](https://newrelic.com/signup) if you don’t have an account.
- **Flask and other dependencies** listed in `requirements.txt`.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mehreentahir16/relicstraurants_chatbot.git
   cd relicstraurants_chatbot
   ```
2. Set up a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Export your OpenAI API key:

   ```bash
   export OPENAI_API_KEY=your-openai-api-key
   ```

## Running the Application

To run the application:

```bash
python3 app.py
```

Once the app is running, open your browser and navigate to `http://127.0.0.1:5000/`, and start chatting.

## Monitoring with New Relic

To integrate your chatbot with New Relic and monitor performance metrics, [install AI monitoring](https://docs.newrelic.com/install/ai-monitoring/) You can also follow the official [guide to learn how to use New Relic AI monitoring to optimize AI chatbot performance](https://newrelic.com/blog/how-to-relic/optimizing-ai-chatbot-performance). 
   

import google.generativeai as genai
import sys
import requests
import random

# ================== API KEYS (keep in config.py for safety) ==================
from config import GEMINI_API_KEY, OPENWEATHER_API_KEY

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Base URL for weather
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Conversation memory
conversation_history = []

# ================== GEMINI RESPONSE ==================
def get_ai_response(user_message, history):
    "Get reply from Gemini in macha style"
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20", system_instruction=" You are a friendly and humorous assistant who speaks in a casual, colloquial style, often using the term 'macha'. Keep responses concise and engaging.")
        chat_session = model.start_chat(
            history=history,

        )
        response = chat_session.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"An error occurred with Gemini API: {e}", file=sys.stderr)
        return "Macha, something went wrong 😅."

# ================== EMOJIFY ==================
def emojize(text):
    emoji_map = {
        "hello": "👋",
        "great": "👍",
        "goodbye": "👋",
        "happy": "😊",
        "sad": "😔",
        "love": "❤",
        "thanks": "🙏",
        "bye": "👋",
        "weather": "🌤",
        "miss you": "🥲",
        "congratulations": "🎉",
        "kiss": "😘"
    }

    words = text.lower().split()
    for word, emoj in emoji_map.items():
        if word in words:
            text += f" {emoj}"

    # Weather keywords
    if "sun" in text.lower() or "clear" in text.lower():
        text += " ☀"
    if "rain" in text.lower():
        text += " 🌧"
    if "cloud" in text.lower() or "overcast" in text.lower():
        text += " ☁"
    if "storm" in text.lower() or "thunder" in text.lower():
        text += " ⛈"

    # Random fun ending
    endings = ["🔥", "😎", "🙌", "😁", "😂", "✨", "🥲"]
    text += " " + random.choice(endings)

    return text.strip()

# ================== WEATHER FETCH ==================
def get_weather(city_name):
    "Fetch weather from OpenWeather API"
    try:
        params = {
            "q": city_name,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(WEATHER_BASE_URL, params=params)
        data = response.json()

        if data.get("cod") == 200:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            message = (
                f"The weather in {city_name.title()} is {description}.\n"
                f"🌡 Temp: {temperature}°C | 💧 Humidity: {humidity}% | 🌬 Wind: {wind_speed} m/s"
            )
            return message
        else:
            return f"Macha, I couldn't find weather for {city_name} 😅."

    except requests.exceptions.RequestException as e:
        print(f"An error occurred with Weather API: {e}", file=sys.stderr)
        return "Weather fetch failed macha 🚨."

# ================== MAIN CHAT LOOP ==================
def start_conversation():
    print("Bot: Yo macha! 😁 I'm your buddy bot. Ask me anything! Type 'bye' to leave me 😒.")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower().strip() == "bye":
                print("Bot: Catch you later macha! 👋🔥 Stay awesome ✨")
                break

            if user_input.lower().startswith("weather in "):
                city_name = user_input.lower().replace("weather in ", "", 1).strip()
                print("Bot: Checking weather... ⏳")
                bot_response = get_weather(city_name)
            else:
                print("Bot: Thinking... 🤔")
                bot_response = get_ai_response(user_input, conversation_history)

            # Add emojis + style
            bot_response_with_emojis = emojize(bot_response)

            print(f"Bot: {bot_response_with_emojis}")

            # Update history
            conversation_history.append({"role": "user", "parts": [{"text": user_input}]})
            conversation_history.append({"role": "model", "parts": [{"text": bot_response}]})

        except (EOFError, KeyboardInterrupt):
            print("\nBot: Ayy macha, you bailed out 😅. Bye 👋")
            sys.exit()

# ================== RUN ==================
if __name__=="__main__":
    start_conversation()
import time
from datetime import datetime
from google import genai
from google.genai.types import GenerateContentConfig, Tool, GoogleSearch
from google.genai.errors import APIError

# =========================
# 🔐 API KEY
# =========================
API_KEY = "AIzaSyDRSLh2dxnlL1OL-TW0nZ_Tm_KWlaNKoNo"

client = genai.Client(api_key=API_KEY)

model_name = "models/gemini-2.5-flash"

# =========================
# 🎯 CREDIT SYSTEM
# =========================
TOTAL_CREDITS = 20
credits_left = TOTAL_CREDITS

# =========================
# 💾 SAVE CHAT HISTORY
# =========================
def save_chat(user, bot):
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}]\n")
        f.write(f"You: {user}\n")
        f.write(f"Bot: {bot}\n")

# =========================
# 🤖 CHAT SESSION
# =========================
chat = client.chats.create(
    model=model_name,
    config=GenerateContentConfig(
        system_instruction="Answer briefly and provide latest real-time information.",
        temperature=0.6,
        max_output_tokens=200,
        tools=[Tool(google_search=GoogleSearch())]  # 🔥 Live Internet Search
    )
)

print("🤖 AI Assistant with Credits + Live Internet")
print(f"🎟 Total Credits: {TOTAL_CREDITS}")
print("Type 'exit' to quit\n")

# =========================
# 🔁 CHAT LOOP
# =========================
while True:

    if credits_left <= 0:
        print("❌ No credits left! Please recharge to continue.")
        break

    print(f"💳 Credits Left: {credits_left}")

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("👋 Chat Ended.")
        break

    print("Bot: Thinking...")

    try:
        response = chat.send_message(user_input)
        reply = response.text

        print("Bot:", reply)

        save_chat(user_input, reply)

        # 🔥 Deduct credit
        credits_left -= 1

    except APIError as e:
        print("❌ API Error:- expire ", e)

    except Exception as e:
        print("⚠️ Error:", e)
    time.sleep(1) 

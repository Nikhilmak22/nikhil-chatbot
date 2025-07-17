from telegram.ext import Updater, MessageHandler, Filters
from gpt4all import GPT4All

# Load your model
model = GPT4All("mistral-7b-openorca.Q4_0.gguf", allow_download=False)

# Load your profile
with open("nikhil_profile.txt", "r", encoding="utf-8") as f:
    personality = f.read()

# Save chat history
chat_history = {}

def reply(update, context):
    user_id = update.message.chat_id
    message = update.message.text

    # Keep user-wise history
    if user_id not in chat_history:
        chat_history[user_id] = []

    prompt = personality + "\n"
    for human, bot in chat_history[user_id]:
        prompt += f"Friend: {human}\nNikhil: {bot}\n"
    prompt += f"Friend: {message}\nNikhil:"

    response = model.generate(prompt, max_tokens=100).strip()
    chat_history[user_id].append((message, response))

    update.message.reply_text(response)

def main():
    # Paste your token here 👇
    TOKEN = "7632457173:AAEB3Ilacgkm4dGSeQBIJ33LfsDfI9M3TVA"

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, reply))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

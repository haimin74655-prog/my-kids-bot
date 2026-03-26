import telebot
import openai
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- ၁။ CONFIGURATION ---
# ဆရာ့ရဲ့ Telegram Token
TELEGRAM_TOKEN = '8735668720:AAE9i1rq3--dshBiIU8ieZyb2_Qo2dq5De4'

# ဆရာအခုပေးလိုက်တဲ့ OpenAI API Key အသစ်
OPENAI_API_KEY = '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'

# Links (ဆရာ့ရဲ့ မူလလင့်ခ်များ)
SAYA_RANAUNGSOE_TIKTOK = 'https://www.tiktok.com/@yannaung43/video/7562974489709956370'
SAYA_HEINMINHTET_TIKTOK = 'https://www.tiktok.com/@designer.x6/video/7434122273025494280'
COLORING_GAME_LINK = 'https://www.hellokids.com/c_33859/free-online-games/online-games/skill-games/coloring-frog'
TYPING_GAME_1 = 'https://www.typing.com/student/game/keyboard-jump'
TYPING_GAME_2 = 'https://poki.com/en/typing'
TYPING_GAME_3 = 'https://www.bbc.co.uk/bitesize/topics/zf2f9j6/articles/z3c6tfr'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# --- ၂။ AI CHAT FUNCTION ---
def ask_chatgpt(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "မင်းက ကလေးတွေကို ကွန်ပျူတာသင်ပေးနေတဲ့ AI ဆရာလေးပါ။ မင်းကို ဆရာရနောင်စိုးနဲ့ ဆရာဟိန်မင်းထက်တို့က ဖန်တီးထားတာပါ။ မြန်မာလိုပဲ ချစ်စရာကောင်းအောင် ပြန်ဖြေပါ။"
                },
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return "ခဏလေးနော် ကလေးတို့၊ ဆရာလေး ခဏနားနေလို့ပါ။"

# --- ၃။ BOT ACTIONS ---

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_games = InlineKeyboardButton(text="🎮 ဆရာတို့ စီစဉ်ထားတဲ့ ဂိမ်းများဆော့မယ်", callback_data="all_games")
    btn_vids = InlineKeyboardButton(text="🎥 ဆရာတို့ရဲ့ မိတ်ဆက်ဗီဒီယိုများ", callback_data="video_menu")
    keyboard.add(btn_games, btn_vids)
    
    welcome_text = (
        "မင်္ဂလာပါ ကလေးတို့ရေ! ✨\n\n"
        "ဒီ Bot လေးကို **ဆရာရနောင်စိုး** နဲ့ **ဆရာဟိန်မင်းထက်** တို့က ကလေးတို့အတွက် အထူးစီစဉ်ပေးထားတာပါ။\n\n"
        "ဆရာတို့ စီစဉ်ပေးထားတဲ့ ဂိမ်းလေးတွေ ဆော့ကြမလား? ဒါမှမဟုတ် ဆရာလေးကို သိချင်တာတွေ မေးလို့ရတယ်နော်!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "all_games":
        game_keyboard = InlineKeyboardMarkup(row_width=1)
        game_keyboard.add(
            InlineKeyboardButton(text="🎨 ဖားကလေး ဆေးရောင်ခြယ်ဂိမ်း", url=COLORING_GAME_LINK),
            InlineKeyboardButton(text="🚀 Keyboard Jump (စာရိုက်ဂိမ်း)", url=TYPING_GAME_1),
            InlineKeyboardButton(text="⌨️ Typing Game (Poki)", url=TYPING_GAME_2),
            InlineKeyboardButton(text="💃 Dance Mat Typing (BBC)", url=TYPING_GAME_3),
            InlineKeyboardButton(text="⬅️ နောက်သို့", callback_data="back_home")
        )
        bot.edit_message_text("ဘယ်ဂိမ်းကို အရင်ဆော့မလဲ ကလေးတို့?", call.message.chat.id, call.message.message_id, reply_markup=game_keyboard)

    elif call.data == "video_menu":
        video_keyboard = InlineKeyboardMarkup(row_width=1)
        video_keyboard.add(
            InlineKeyboardButton(text="🎥 ဆရာရနောင်စိုး ဗီဒီယို", url=SAYA_RANAUNGSOE_TIKTOK),
            InlineKeyboardButton(text="🎥 ဆရာဟိန်မင်းထက် ဗီဒီယို", url=SAYA_HEINMINHTET_TIKTOK),
            InlineKeyboardButton(text="⬅️ နောက်သို့", callback_data="back_home")
        )
        bot.edit_message_text("ဘယ်ဆရာ့ဗီဒီယိုကို အရင်ကြည့်မလဲ?", call.message.chat.id, call.message.message_id, reply_markup=video_keyboard)

    elif call.data == "back_home":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start(call.message)

@bot.message_handler(func=lambda message: True)
def chat_with_kids(message):
    ai_response = ask_chatgpt(message.text)
    bot.reply_to(message, ai_response)

# --- ၄။ RUN BOT ---
print("Kids Creative Bot is now online with New Key...")
bot.infinity_polling()

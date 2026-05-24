import telebot
import google.generativeai as genai

# ====== SHU YERGA O'ZINGIZNING KALITLARINGIZNI QO'YING ======
BOT_TOKEN = "7330541994:AAExampleToken..."  # BotFather bergan token
API_KEY = "AIzaSyDTZ8Wha5VLt-kC88jWeEZnkjEZgCBLufE"  # Google API kalit
# ==========================================================

# Bot va AI konfiguratsiyasi
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 Assalomu alaykum! Quiz-Generator botga xush kelibsiz.\n\n"
        "📝 Menga ichida test savollari bo'lgan matnli (.txt) fayl yuboring. "
        "Men Google Gemini AI yordamida har bir savolga kamida 100 ta so'zdan iborat "
        "batafsil tushuntirish va quiz formatidagi javoblarni tayyorlab beraman!"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        # Faylni yuklab olish
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Fayl matnini o'qish
        user_text = downloaded_file.decode('utf-8')
        
        bot.reply_to(message, "⏳ Savollar qayta ishlanmoqda, iltimos biroz kuting...")
        
        # Sun'iy intellektga buyruq (Prompt) yuborish
        prompt = (
            f"Quyidagi matn ichidagi test savollarini tahlil qil. Har bir savol uchun "
            f"to'g'ri javobni ko'rsat va har bir savolga alohida-alohida KAMIDA 100 TA SO'ZDAN iborat "
            f"batafsil, ilmiy va tushunarli izoh yozib ber:\n\n{user_text}"
        )
        
        response = model.generate_content(prompt)
        ai_response = response.text
        
        # Agar javob juda uzun bo'lsa, Telegram qoidasiga ko'ra bo'lib yuborish
        if len(ai_response) > 4096:
            for x in range(0, len(ai_response), 4096):
                bot.send_message(message.chat.id, ai_response[x:x+4096])
        else:
            bot.send_message(message.chat.id, ai_response)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {str(e)}\nFayl formati .txt ekanligiga ishonch hosil qiling.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "💡 Iltimos, menga savollar yozilgan .txt formatidagi fayl yuboring.")

# Botni uzluksiz ishga tushirish
bot.infinity_polling()

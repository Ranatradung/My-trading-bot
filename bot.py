from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = '8794204046:AAFYu42YI-HrJB3_Qq3w8gJOwXlk9UR6T4g'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.upper()
    
    # إذا كانت الرسالة "GBP" أو "GOLD"
    if text in ["GBP", "GOLD"]:
        context.user_data['pair'] = text
        await update.message.reply_text(f"تم اختيار {text}. الآن أرسلي السعر الحالي:")
        return

    # إذا كان المستخدم قد اختار العملة سابقاً وأرسل السعر
    if 'pair' in context.user_data:
        try:
            price = float(text)
            pair = context.user_data['pair']
            
            # معادلات السكالبينج
            if pair == 'GBP':
                sig = "شراء" if price % 0.100 < 0.050 else "بيع"
                tp, sl = (price + 0.050, price - 0.025) if sig == "شراء" else (price - 0.050, price + 0.025)
            else:
                sig = "شراء" if price % 4.0 < 2.0 else "بيع"
                tp, sl = (price + 2.0, price - 1.0) if sig == "شراء" else (price - 2.0, price + 1.0)

            msg = (f"⚡️ تحليل ({pair}):\n\n"
                   f"السعر: {price:.3f}\n"
                   f"الاتجاه: {sig}\n"
                   f"الهدف: {tp:.3f}\n"
                   f"الستوب: {sl:.3f}\n\n"
                   f"للتحليل من جديد، اكتبي GBP أو GOLD.")
            
            await update.message.reply_text(msg)
            del context.user_data['pair'] # مسح الاختيار للبدء من جديد
        except:
            await update.message.reply_text("يرجى إرسال السعر كأرقام فقط.")
    else:
        await update.message.reply_text("أهلاً رنا! ابدئي بكتابة: GBP أو GOLD")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل الآن بدون تعقيدات! اكتبي GBP أو GOLD")
    app.run_polling()

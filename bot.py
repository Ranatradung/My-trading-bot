from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = '8794204046:AAFYu42YI-HrJB3_Qq3w8gJOwXlk9UR6T4g'

# مراحل التحليل
CHOOSING_PAIR, DEMAND, SUPPLY, TRIGGER = range(4)

async def start(update, context):
    # خيارات العملات
    reply_keyboard = [['GBP', 'GOLD']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(
        "أهلاً رنا! 🚀\nأنا مساعدك الذكي للتداول.\n"
        "يرجى اختيار العملة التي تودين تحليلها:",
        reply_markup=markup
    )
    return CHOOSING_PAIR

async def choose_pair(update, context):
    context.user_data['pair'] = update.message.text
    await update.message.reply_text(f"تم اختيار {context.user_data['pair']}.\nالآن أرسلي 'منطقة الطلب' (Demand Zone):", reply_markup=ReplyKeyboardRemove())
    return DEMAND

async def get_demand(update, context):
    context.user_data['demand'] = float(update.message.text)
    await update.message.reply_text("ممتاز، الآن أرسلي 'منطقة العرض' (Supply Zone):")
    return SUPPLY

async def get_supply(update, context):
    context.user_data['supply'] = float(update.message.text)
    await update.message.reply_text("الآن أرسلي 'سعر الزناد' (Trigger Price - STRIKE90):")
    return TRIGGER

async def get_trigger(update, context):
    trigger = float(update.message.text)
    pair = context.user_data['pair']
    demand = context.user_data['demand']
    supply = context.user_data['supply']
    
    msg = (f"⚡️ تحليل الدمج الذكي ({pair}):\n\n"
           f"المنطقة: {demand} - {supply}\n"
           f"الزناد: {trigger}\n\n")
    
    if demand <= trigger <= supply:
        msg += "✅ حالة المنطقة: صالحة للدخول.\n🎯 القرار: انتظري ملامسة الزناد للدخول!"
    else:
        msg += "⚠️ تحذير: الزناد بعيد عن المناطق، لا تدخلي!"
    
    await update.message.reply_text(msg + "\n\nلتحليل جديد اكتبي /start")
    return ConversationHandler.END

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_PAIR: [MessageHandler(filters.TEXT, choose_pair)],
            DEMAND: [MessageHandler(filters.TEXT, get_demand)],
            SUPPLY: [MessageHandler(filters.TEXT, get_supply)],
            TRIGGER: [MessageHandler(filters.TEXT, get_trigger)],
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    app.add_handler(conv_handler)
    app.run_polling()

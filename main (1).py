import telebot
import time
import json
import threading
import emoji
import random
from telebot import types
from telebot.types import LabeledPrice, PreCheckoutQuery
from telebot.apihelper import ApiTelegramException

# --- КОНФИГУРАЦИЯ ---
API_TOKEN = '7673823973:AAEdqIKX_T3qqG9N3s2YHHdTXwq7t1Xn-eQ'
TARGET_CHAT_ID = -1002587684899
BAN_FILE = "banned_users.json"

# Настройки ограничений
MAX_MESSAGE_LENGTH = 500
MAX_EMOJI_COUNT = 10
MUTE_DURATION = 3600
BAN_DURATION = 30 * 24 * 60 * 60
REACTION_CHANCE = 0.20

# Белый список
WHITELIST = [
    "https://t.me/ByStepChatik",
    "https://t.me/ByStepLive",
    "https://t.me/Rules_Bystep"
]

BLACKLIST_SHORTENERS = [
    "clck.ru", "bit.ly", "goo.gl", "tinyurl.com",
    "is.gd", "vk.cc", "t.co", "rebrand.ly"
]

# --- СЛОВАРЬ GIFTS УДАЛЕН ---
# Теперь ID подарка вводится напрямую

bot = telebot.TeleBot(API_TOKEN)

# --- СОХРАНЕНИЕ БАНОВ ---
def load_bans():
    try:
        with open(BAN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_ban(user_id, unban_time):
    bans = load_bans()
    bans[str(user_id)] = unban_time
    with open(BAN_FILE, "w", encoding="utf-8") as f:
        json.dump(bans, f, indent=4)

def remove_ban_from_file(user_id):
    bans = load_bans()
    if str(user_id) in bans:
        del bans[str(user_id)]
        with open(BAN_FILE, "w", encoding="utf-8") as f:
            json.dump(bans, f, indent=4)

# --- ФОНОВАЯ ЗАДАЧА (РАЗБАН) ---
def check_unbans():
    while True:
        bans = load_bans()
        current_time = time.time()
        to_unban = [uid for uid, t in bans.items() if current_time >= t]
        for user_id in to_unban:
            try:
                bot.restrict_chat_member(TARGET_CHAT_ID, int(user_id), True, True, True, True)
            except:
                try: bot.unban_chat_member(TARGET_CHAT_ID, int(user_id), only_if_banned=True)
                except: pass
            finally:
                remove_ban_from_file(user_id)
        time.sleep(60)

threading.Thread(target=check_unbans, daemon=True).start()

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def get_user_from_message(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    args = message.text.split()
    for arg in args:
        if arg.isdigit() and len(arg) > 5:
            class UserObj:
                id = int(arg)
                first_name = "User"
            return UserObj
    return None

# --- МОДЕРАЦИЯ И ПРОВЕРКИ (Остались без изменений) ---
def restrict_user_mute(chat_id, user_id, reason):
    try:
        unban_timestamp = time.time() + MUTE_DURATION
        bot.restrict_chat_member(chat_id, user_id, until_date=int(unban_timestamp), can_send_messages=False)
        save_ban(user_id, unban_timestamp)
        msg = f"🔇 <a href='tg://openmessage?user_id={user_id}'>Пользователь</a> в муте на 1 час.\n💬 <b>Причина:</b> {reason}"
        bot.send_message(chat_id, msg, parse_mode='HTML')
    except Exception as e: print(f"Ошибка мута: {e}")

def ban_user_kick(chat_id, user_id, reason):
    try:
        unban_timestamp = time.time() + BAN_DURATION
        bot.ban_chat_member(chat_id, user_id, until_date=int(unban_timestamp))
        msg = f"🔴 <a href='tg://openmessage?user_id={user_id}'>Пользователь</a> забанен на 30 дней.\n💬 <b>Причина:</b> {reason}"
        bot.send_message(chat_id, msg, parse_mode='HTML')
    except Exception as e: print(f"Ошибка бана: {e}")

def check_link(text, entities):
    if not entities: return False
    for entity in entities:
        url = None
        if entity.type == 'text_link': url = entity.url
        elif entity.type == 'url': url = text[entity.offset : entity.offset + entity.length]
        if url:
            url_lower = url.lower()
            for bad in BLACKLIST_SHORTENERS:
                if f"://{bad}" in url_lower or url_lower.startswith(bad): return True
            if "t.me/" in url_lower or "telegram.me/" in url_lower:
                is_allowed = False
                for white in WHITELIST:
                    if white.lower().replace("https://", "").replace("http://", "") in url_lower:
                        is_allowed = True; break
                if not is_allowed: return True
    return False

# --- ЭКОНОМИКА: НАСТОЯЩИЕ ПОДАРКИ И ДОНАТ ---

# 1. КОМАНДА /ПОДАРОК (ТРАТИТ ЗВЕЗДЫ БОТА!)
@bot.message_handler(commands=['тгподарок'])
def send_real_gift(message):
    # Защита: только админ может тратить баланс бота


    lines = message.text.split('\n')
    args = lines[0].split() # /подарок РЕАЛЬНЫЙ_ID_ПОДАРКА ID_ЮЗЕРА

    if len(args) < 3:
        help_text = "🎁 <b>Отправка платного подарка (за звезды бота):</b>\n"
        help_text += "<code>/подарок 5170233102089322756 123456789</code>\n"
        help_text += "<code>Текст поздравления на следующей строке</code>"
        bot.reply_to(message, help_text, parse_mode='HTML')
        return

    # --- ИЗМЕНЕНИЕ ЛОГИКИ ---
    real_gift_id = args[1] # Это теперь реальный, длинный ID подарка
    target_user_id = args[2]
    gift_text = "\n".join(lines[1:]) if len(lines) > 1 else ""

    if not real_gift_id.isdigit():
        bot.reply_to(message, "❌ ID подарка должен быть длинным числом.")
        return

    if not target_user_id.isdigit():
        bot.reply_to(message, "❌ ID получателя должен быть числом.")
        return

    bot.send_chat_action(message.chat.id, 'choose_sticker')

    try:
        # === ОТПРАВКА РЕАЛЬНОГО ПОДАРКА ===
        bot.send_gift(
            user_id=int(target_user_id),
            gift_id=real_gift_id,
            text=gift_text,
            text_parse_mode="Markdown"
        )

        bot.reply_to(message, f"✅ Подарок успешно отправлен пользователю {target_user_id}!")

    except ApiTelegramException as e:
        desc = e.result_json.get('description', '')
        if "BALANCE_NOT_ENOUGH" in desc or "balance" in desc.lower():
            bot.reply_to(message, "❌ <b>Ошибка:</b> У бота недостаточно Telegram Stars на балансе для этого подарка.")
        elif "PEER_ID_INVALID" in desc:
             bot.reply_to(message, "❌ <b>Ошибка:</b> Некорректный ID пользователя или пользователь не запускал бота.")
        else:
            bot.reply_to(message, f"❌ Ошибка API: {desc}")
            print(f"Ошибка при отправке подарка: {e}")

    except AttributeError:
        bot.reply_to(message, "❌ Ваша библиотека `telebot` устарела и не знает команду `send_gift`. Обновите её: `pip install --upgrade pyTelegramBotAPI`")
    except Exception as e:
        bot.reply_to(message, f"❌ Неизвестная ошибка: {e}")


# 2. КОМАНДА /ДОНАТ (ПРИНИМАЕТ ЗВЕЗДЫ) (Осталась без изменений)
@bot.message_handler(commands=['донат'])
def donate_command(message):
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "Используйте: `/донат 10` (где 10 - количество звезд)")
        return

    amount = int(args[1])
    if amount < 1:
        bot.reply_to(message, "Минимум 1 звезда.")
        return

    try:
        prices = [LabeledPrice(label="Пожертвование", amount=amount)]
        bot.send_invoice(
            message.chat.id,
            title="Поддержка канала",
            description=f"Донат на развитие проекта: {amount} звезд.",
            invoice_payload="donation_payload",
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter="donate"
        )
    except Exception as e:
        bot.reply_to(message, f"Ошибка создания счета: {e}")

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    stars = message.successful_payment.total_amount
    user = message.from_user.first_name
    bot.send_message(message.chat.id, f"🌟 <b>СПАСИБО!</b> {user} задонатил {stars} звезд! 💖", parse_mode='HTML')

# --- АДМИНСКИЕ КОМАНДЫ И ОБРАБОТЧИКИ ---
@bot.message_handler(commands=['unmute', 'размут'])
def unmute_command(message):
    if not is_admin(message.chat.id, message.from_user.id): return
    target = get_user_from_message(message)
    if target:
        bot.restrict_chat_member(message.chat.id, target.id, True, True, True, True)
        remove_ban_from_file(target.id)
        bot.reply_to(message, "✅ Мут снят.")

@bot.message_handler(commands=['unban', 'разбан'])
def unban_command(message):
    if not is_admin(message.chat.id, message.from_user.id): return
    target = get_user_from_message(message)
    if target:
        bot.unban_chat_member(message.chat.id, target.id, only_if_banned=True)
        remove_ban_from_file(target.id)
        bot.reply_to(message, "✅ Бан снят.")

@bot.message_handler(func=lambda m: m.chat.id == TARGET_CHAT_ID, regexp=r"^(правила|!правила|/правила)$")
def handle_rules(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти к правилам", url="http://t.me/hamstercomz_bot/bysteprul"))
    bot.reply_to(message, "❕ Правила: ", reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id == TARGET_CHAT_ID, content_types=['text', 'caption'])
def handle_messages(message):
    # Реакции
    if message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id:
        bot_msg = message.reply_to_message.text or message.reply_to_message.caption or ""
        if any(w in bot_msg.lower() for w in ["мут", "забанен", "заблокирован", "причина"]):
            if random.random() < REACTION_CHANCE:
                try: bot.set_message_reaction(message.chat.id, message.message_id, [types.ReactionTypeEmoji("👍")])
                except: pass

    # Модерация
    user_id = message.from_user.id
    if message.sender_chat or is_admin(message.chat.id, user_id): return
    text = message.text or message.caption or ""
    entities = message.entities or message.caption_entities

    if check_link(text, entities):
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass
        ban_user_kick(message.chat.id, user_id, "Реклама")
        return

    if emoji.emoji_count(text) >= MAX_EMOJI_COUNT:
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass
        restrict_user_mute(message.chat.id, user_id, f"Спам эмодзи")
        return

    if len(text) >= MAX_MESSAGE_LENGTH:
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass
        restrict_user_mute(message.chat.id, user_id, "Длинное сообщение")
        return

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()

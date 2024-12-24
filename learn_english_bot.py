import telebot
import json
import random
token = "7478834124:AAHp2HhLbO7AzrCk9PvQBVKhnSWN7Lp39kc"

bot = telebot.TeleBot(token)
file = open("data.json", "r", encoding = "UTF-8")
word_ids = json.load(file)
file.close()
@bot.message_handler(["start"])
def handle_start(message):
    print("Hi")
    bot.send_message(message.chat.id, "Hello")


def true(message):
    return True


@bot.message_handler(["add_word"])
def handle_add_word(message):
    english_word = message.text.split(" ")[2]
    russian_word = message.text.split(" ")[1]
    if str(message.chat.id) in word_ids:
        words_user = word_ids[str(message.chat.id)]
        words_user[russian_word] = english_word
    else:
        word_ids[str(message.chat.id)] = {russian_word : english_word}

    file = open("data.json", "w", encoding = "UTF-8")
    json.dump(word_ids, file, ensure_ascii = False, indent = 4)
    file.close()



@bot.message_handler(["show_words"])
def handle_show_words(message):
    words = ""
    if str(message.chat.id) in word_ids:
        for word in word_ids[str(message.chat.id)]:
            words += word + ": " + word_ids[str(message.chat.id)][word] + "\n"
        bot.send_message(message.chat.id, words)
    else:
        bot.send_message(message.chat.id, "Sorry, you have no words")


@bot.message_handler(["game"])
def handle_game(message):
    game(message)

def answer_for_game(message, correct_answer):
    if message.text == correct_answer:
        bot.send_message(message.chat.id, "Good Job!")
    else:
        bot.send_message(message.chat.id, "Incorrect! The correct answer is " + correct_answer)

    game(message)

def game(message):
    list = []
    print("hello")
    words = word_ids[str(message.chat.id)]
    for word in words:
        list.append(word)

    word_to_guess = list[random.randint(0, len(list) - 1)]
    correct_answer = words[word_to_guess]
    bot.send_message(message.chat.id, "what is the translation of " + word_to_guess)
    bot.register_next_step_handler_by_chat_id(message.chat.id, answer_for_game, correct_answer)
@bot.message_handler(func = true)
def handle_random_text(message):
    print(message.text)
    if message.text.lower() == "hi":
        bot.send_message(message.chat.id, "Hello")

    elif message.text.lower() == "how are you doing?":
        bot.send_message(message.chat.id, "Good, how are you?")

    else:
        bot.send_message(message.chat.id, "Sorry I don't understand")


bot.polling()
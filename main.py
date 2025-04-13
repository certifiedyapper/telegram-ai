import telebot
from telebot.types import Message

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def detect_image(input_path, model):
    np.set_printoptions(suppress=True)
    model = load_model(model, compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(input_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    return index, confidence_score


bot = telebot.TeleBot('!bot token here!')

@bot.message_handler(commands=['start'])
def start_cnd(message: Message):
    bot.send_message(message.chat.id, 'Hello dear traveller, send me a picture of a car symbole between volkswagen, nissan, toyota and bmw and I, a divine wizard, shall tell thy kind what car brand thy symbole belongs to !!!!1!')


@bot.message_handler(content_types= 'photo')
def photo_cmd(message: Message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Thats not a picture, traveller')
    
    filename = f"photo_{message.from_user.id}.png"
    fileinfo = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(fileinfo.file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(file)

    old_message = bot.send_message(message.chat.id, " Your picture has been downloaded, please waith")

    index, score = detect_image(filename, "keras_model.h5")
    if score < 0.90:
        return bot.send_message(message.chat.id, "sorry I'm a little slow on this one traveller, figure it out on your own ;)")
    if index == 0:
        return bot.send_message(message.chat.id, f"okay well it's a toyota ,traveller, im sure with {round(score * 100,1)}% of my divine soul")
    elif index == 1:
        return bot.send_message(message.chat.id, f"alright traveller, well this is a nissan , it literally says on the symbol , im sure with {round(score * 100,1)}% of my divine soul")
    elif index == 2:
        return bot.send_message(message.chat.id, f"alright traveller, well this is a bmw, im sure with {round(score * 100,1)}% of my divine soul")
    elif index == 3:
        return bot.send_message(message.chat.id, f"alright traveller, well this is a volkswage I am sure with {round(score * 100,1)}% of my divine soul")
    bot.delete_message(old_message.chat.id, old_message.id)




bot.infinity_polling()

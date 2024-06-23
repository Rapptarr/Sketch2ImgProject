import telebot
import requests
import webuiapi

from telebot import types
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from g4f.client import Client
from deep_translator import GoogleTranslator

TOKEN = "7362722759:AAHJZ9IJrgi55briADuAfn4czzHKDesQfYk"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Приступить к работе")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет! Давайте начнем работу с эскизами. Нажмите 'Приступить к работе', чтобы начать.",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Приступить к работе':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Ввести промпт вручную')
        btn2 = types.KeyboardButton('Не вводить промпт')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Хотите ли вы ввести промпт вручную?', reply_markup=markup)

    elif message.text == 'Ввести промпт вручную':
        bot.send_message(message.from_user.id, "Пожалуйста, введите ваш промпт:")
        bot.register_next_step_handler(message, prompt_choice)

    elif message.text == 'Не вводить промпт':
        choose_variant(message, None)


def prompt_choice(message):
    user_prompt = message.text
    translated_prompt = GoogleTranslator(source='auto', target='en').translate(user_prompt)
    choose_variant(message, translated_prompt)


def choose_variant(message, user_prompt):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Сохранить контур')
    btn2 = types.KeyboardButton('Сохранить структуру')
    btn3 = types.KeyboardButton('Сохранить глубину')
    btn4 = types.KeyboardButton('Сохранить позу')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id, 'Сделайте выбор', reply_markup=markup)

    bot.register_next_step_handler(message, process_variant, user_prompt)


def process_variant(message, user_prompt):
    if message.text in ['Сохранить контур', 'Сохранить структуру', 'Сохранить глубину', 'Сохранить позу']:
        if message.text == 'Сохранить контур':
            mode = 'lineart_realistic'
            model = 'control_v11p_sd15_lineart [43d4be0d]'
            weights = (0.7, 0.3)
        elif message.text == 'Сохранить структуру':
            mode = 'depth_anything'
            model = 'control_v11f1p_sd15_depth [cfd03158]'
            weights = (0.4, 0.6)
        elif message.text == 'Сохранить глубину':
            mode = 'normal_bae'
            model = 'control_v11p_sd15_normalbae [316696f1]'
            weights = (0.5, 0.5)
        elif message.text == 'Сохранить позу':
            mode = 'openpose_full'
            model = 'control_v11p_sd15_openpose [cab727d4]'
            weights = (0.6, 0.4)

        bot.send_message(message.from_user.id, "Отправьте ваш эскиз")
        bot.register_next_step_handler(message, process_photo, *weights, mode, model, user_prompt)


def process_photo(message, a, b, c, d, user_prompt):
    if message.content_type == 'photo':
        photo_data = message.photo[-1]
        file_id = photo_data.file_id
        file_path = bot.get_file(file_id)
        photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path.file_path}"

        processor = BlipProcessor.from_pretrained("unography/blip-long-cap")
        model = BlipForConditionalGeneration.from_pretrained("unography/blip-long-cap")
        raw_image = Image.open(requests.get(photo_url, stream=True).raw).convert('RGB')
        text = "a photography of"
        inputs = processor(raw_image, text, return_tensors="pt")
        out = model.generate(**inputs)
        caption = processor.decode(out[0], skip_special_tokens=True)

        client = Client()
        prompt_request = (
            "Помоги написать промпт по следующим правилам. Ты создаешь промпт для обработки изображения.  "
            "Правила: "
            "1) Составляй промпт из отдельных слов или коротких словосочетаний перечисляемых через запятую на английском языке "
            "2) В промпте не должно быть упоминания любых стилей кроме реалистичного. "
            "3) Промпт должен содержать описание для разукрашивания того, что на изображении. "
            "4) Улучшение естественного освещения и теней. "
            "5) Избегание искусственных фильтров и преувеличенных эффектов. "
            "6) Сохранение оригинальных деталей изображения. "
            "7) Сосредоточение на четкости и реалистичной текстуре. "
            "8) Подчеркивание аутентичных цветов и оттенков. "
            "9) Субтильное улучшение глубины и перспективы. "
            "10) Исключение мультяшных или сюрреалистичных элементов. "
            "11) Удали упоминания того что изображение нарисовано карандашом, либо замени это на реалистичный стиль. "
            "12) Итоговое изображение должно выглядеть как фотография."
            "13) ИСКЛЮЧИ ПОЛЬНОСТЬЮ КИТАЙСКИЙ ЯЗЫК ИЗ СВОИХ ОТВЕТОВ"
            "В ответе напиши мне только промпт. "
        )

        prompt = prompt_request + caption

        def gpt(prompt):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        detailed_prompt = gpt(prompt)
        additional_prompt = "contrast, colorful, photorealistic image, high detalization, clarity, blurred background, 4k, realistic proportions, natural proportions, beautiful body and face, smooth the drawn lines, remove extra lines"

        if user_prompt:
            final_prompt = user_prompt + ', ' + additional_prompt
        else:
            final_prompt = additional_prompt + ' ' + detailed_prompt

        print(final_prompt)

        api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)
        options = {'sd_model_checkpoint': '0001softrealistic_v187xxx.safetensors [877aac4a95]'}
        api.set_options(options)

        image = raw_image
        unit1 = webuiapi.ControlNetUnit(image=image, module=c, model=d, weight=a)
        unit2 = webuiapi.ControlNetUnit(image=image, module='lineart_standard',
                                        model='control_v11p_sd15_lineart [43d4be0d]', weight=b)

        result = api.img2img(
            prompt=final_prompt,
            negative_prompt="Unrealistic styles, naked body parts, nude body parts, person without clothes, bare chest, bare legs cartoon, anime, black and white, non-contrast, ugly face, ugly body shape, anatomical errors, disproportionate body parts, pale colors, not according to image, effects that may make the image blurry or unrealistic, ugly eyes, unreal eyes",
            images=[image],
            width=512,
            height=512,
            controlnet_units=[unit1, unit2],
            sampler_name="Euler a",
            cfg_scale=7,
        )
        generated_image = result.image
        generated_image.save('generated_image.png')

        with open('generated_image.png', 'rb') as img:
            bot.send_photo(message.from_user.id, img, caption="Ваше сгенерированное изображение")

bot.polling(none_stop=True, interval=0)
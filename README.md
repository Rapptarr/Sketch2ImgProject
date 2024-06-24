# Sketch2ImgProject

## Описание проекта
В этом проекте мы разработали структуру преобразования эскизов в реалистичные изображения и интегрировали в проект телеграм-бота. Бот использует различные модели машинного обучения и API для достижения этой цели.

## Введение
Этот телеграм-бот позволяет пользователям загружать свои эскизы или черно-белые рисунки и получать окрашенную, реалистичную версию изображения. Пользователи могут выбрать различные варианты преобразования и ввести пользовательский промпт или позволить боту сгенерировать его автоматически.

## Установка
- Переходим по ссылке и скачиваем [Stability Matrix](https://github.com/LykosAI/StabilityMatrix)
- Во избежание технических проблем устанавливать рекомендуем по пути, установленному по умолчанию.
- В Stability Matrix устанавливаем модель Stable Diffusion WebUI от AUTOMATIC1111.
- В Stable Diffusion устанавливаем блок Control Net https://github.com/Mikubill/sd-webui-controlnet

![Установка модели](https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/Contr1.png)

- Скачиваем интересующие модели Control Net [здесь](https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main)

- В нашей работе использовались модели lineart, depth, normalmap, openpose

## Запуск программы
- Устанавливаем необходимые библиотеки
```
import telebot
import requests
import webuiapi

from telebot import types
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from g4f.client import Client
from deep_translator import GoogleTranslator
```

- Запускаем файл с кодом v2.py в pycharm

## Функции
- Автоматическое улучшение эскизов: Преобразует эскизы в реалистичные изображения.
- Пользовательские промпты: Пользователи могут вводить свои собственные промпты для преобразования изображений.
- Несколько режимов: Пользователи могут выбирать разные стили и уровни улучшения.
- Обработка в реальном времени: Быстро обрабатывает и выдает улучшенное изображение.

## Архитектура
- Telegram API: Обрабатывает сообщения и взаимодействие с пользователями.
- Transformers и BLIP: Используются для описания изображений и генерации детализированных промптов.
- WebUIAPI: Интегрируется с системой улучшения изображений.
- ControlNet: Применяет специфические модели улучшения на основе выбора пользователя.
- Client (GPT-3.5-turbo): Генерирует детализированные и уточненные промпты для улучшения изображений.

## Используемые библиотеки и инструменты
- Telebot: Для создания телеграм-бота и обработки взаимодействия с пользователями.
- Requests: Для загрузки изображений из Telegram.
- Transformers: Для описания изображений и генерации промптов.
- PIL: Для обработки изображений.
- WebUIAPI: Для взаимодействия с моделями улучшения изображений.
- Client (GPT-3.5-turbo): Для генерации промптов.

##  Детальные шаги
- Запуск бота: Пользователь инициирует взаимодействие, нажав "Приступить к работе".

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%821.jpg" width="315" height="620"> <img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%822.jpg" width="315" height="620">

- Ввод промпта: Пользователь может выбрать ввод пользовательского промпта или пропустить этот шаг.

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%823.jpg" width="315" height="620">

- Выбор варианта: Пользователь выбирает один из четырех вариантов переработки изображения.

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%825.jpg" width="315" height="620">

- Загрузка эскиза: Пользователь загружает свой эскиз для обработки.

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%824.jpg" width="315" height="620">
  
- Получение улучшенного изображения: Бот обрабатывает изображение и возвращает улучшенную версию.

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%826.jpg" width="315" height="620">

##  Примеры работы

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%9F%D0%BE%D1%80%D1%88%D0%B51.jpg" width="750" height="620"> <img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%9F%D0%BE%D1%80%D1%88%D0%B52.jpg" width="630" height="620">
<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%9F%D0%BE%D1%80%D1%88%D0%B53.jpg" width="630" height="620">

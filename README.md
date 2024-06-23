# Sketch2ImgProject

## Описание проекта
В этом проекте мы разработали структуру преобразования эскизов в реалистичные изображения и интегрировали в проект телеграм-бота. Бот использует различные модели машинного обучения и API для достижения этой цели.

## Введение
Этот телеграм-бот позволяет пользователям загружать свои эскизы или черно-белые рисунки и получать окрашенную, реалистичную версию изображения. Пользователи могут выбрать различные варианты преобразования и ввести пользовательский промпт или позволить боту сгенерировать его автоматически.

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

<img src="https://github.com/Rapptarr/Sketch2ImgProject/blob/main/screenshots/%D0%91%D0%BE%D1%821.jpg" width="200" height="600">

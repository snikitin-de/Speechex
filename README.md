# 💻 Speechex

💻 💬 Бот «Speechex» для _Telegram_ преобразует голосовые и видео сообщения в текст, обеспечивая удобное чтение содержания аудио и видео.

<div align="center"><img src="https://github.com/snikitin-de/Speechex/assets/25394427/9ece3e55-adf0-445a-b961-831cd6f149b3"></div>

## 📄 Описание

### 💻 Работа с программой 

При добавлении бота в группу, он будет автоматически преобразовывать голосовые сообщения и видео кружочки в текст.

Как только бот увидит сообщения нужного типа, он сразу же ответит на него сообщением `[...]`, это значит, что бот начал обрабатывать сообщение.

![Пример начала обработки сообщения](https://github.com/snikitin-de/Speechex/assets/25394427/4a258227-f772-4d2b-a22c-d2ef6d6b2484)

После обработки сообщения, бот отредактирует его и выведет результат распознавания:

![Пример распознавания](https://github.com/snikitin-de/Speechex/assets/25394427/9ece3e55-adf0-445a-b961-831cd6f149b3)

Также доступна команда `/text`, которая позволяет преобразовать в текст не только голосовые сообщения и видео кружочки в текст, но и аудио и видео сообщения. Для этого необходимо ответить на сообщение, которое хотите преобразовать в текст, командой `text`.

![Пример использования команды](https://github.com/snikitin-de/Speechex/assets/25394427/fe3a9d6f-7f6d-4246-a1d5-26121143ac35)

## 🔧 Техническая часть

* Для создания _Telegram_ бота используется библиотека **pyTelegramBotAPI**.
* Для преобразования речи в текст используется улучшенная реализация модели [Whisper](https://github.com/openai/whisper) от OpenAI — [faster_whisper](https://github.com/SYSTRAN/faster-whisper).

### 🧩 Архитектура

Структура каталога проекта:

![Структура каталога проекта](https://github.com/snikitin-de/Speechex/assets/25394427/2691c4bb-eddb-41b8-9be3-1ab5c6c9a259)

### 📘 Требования

* [Docker](https://www.docker.com/);

### 💿 Установка

To run the program, enter the command into the terminal: 

Для запуска Docker-контейнера введите следующую команду в терминал:

`docker run -d -v speechex_model:/root/.cache/huggingface/hub/ -e TELEGRAM_BOT_TOKEN=<TOKEN> snikitinde/speechex`

Доуступные переменные окружения:

* TELEGRAM_BOT_TOKEN — токен Telegram бота;
* WHISPER_MODEL — размер модели. По умолчанию `small`.
* WHISPER_DEVICE — устройство, на котором будет работать модель: `cuda`, `cpu`. По умолчанию `cpu`.
* WHISPER_COMPUTE_TYPE — квантование. По умолчанию `int8`.
* WHISPER_BEAM_SIZE — количество лучей, используемых при поиске лучей при отборе проб при нулевой температуре. По умолчанию `5`.

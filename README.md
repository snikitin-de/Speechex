# Speechex
Bot for converting audio, video and video note messages from Telegram to text.

## Requirements

* [Docker](https://www.docker.com/);

## Usage

To run the program, enter the command into the terminal: 

`docker run -d -v speechex_model:/root/.cache/huggingface/hub/ -e TELEGRAM_BOT_TOKEN=<TOKEN> snikitinde/speechex`

The available environment variables:

* TELEGRAM_BOT_TOKEN — token for Telegram bot;
* WHISPER_MODEL — model size. Default is `small`.
* WHISPER_DEVICE — the device on which the model is processed: `cuda`, `cpu`. Default is `cpu`.
* WHISPER_COMPUTE_TYPE — quantization. Default is `int8`.
* WHISPER_BEAM_SIZE — the number of beams to use in beam search when sampling with zero temperature. Default is `5`.

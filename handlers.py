import telebot
import main


class ExceptionHandler(telebot.ExceptionHandler):
    def handle(self, exception):
        main.logger.error(exception)
        return True

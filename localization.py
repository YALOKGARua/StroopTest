class Localization:
    def __init__(self, language="english"):
        self.colors = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "purple": (128, 0, 128),
            "black": (0, 0, 0)
        }
        self.translations = {
            "english": {
                "start": "Press any key to start",
                "avg_time": "Average time: {avg_time:.2f} sec",
                "coefficient": "Coefficient: {coefficient:.2f}",
                "accuracy": "Accuracy: {accuracy:.2f}%",
                "correct": "Correct!",
                "incorrect": "Incorrect!",
                "restart": "Restart",
                "menu": "Main Menu",
                "play": "Play",
                "settings": "Settings",
                "exit": "Exit",
                "language": "Language",
                "resolution": "Resolution",
                "display_mode": "Display Mode",
                "back": "Back",
                "russian": "Russian",
                "ukrainian": "Ukrainian",
                "english": "English",
                "fullscreen": "Fullscreen",
                "noframe": "Fullscreen No Border",
                "windowed": "Windowed",
                "colors": {
                    "red": "Red",
                    "green": "Green",
                    "blue": "Blue",
                    "yellow": "Yellow",
                    "purple": "Purple",
                    "black": "Black"
                }
            },
            "russian": {
                "start": "Нажмите любую клавишу для начала",
                "avg_time": "Среднее время: {avg_time:.2f} сек",
                "coefficient": "Коэффициент: {coefficient:.2f}",
                "accuracy": "Точность: {accuracy:.2f}%",
                "correct": "Правильно!",
                "incorrect": "Неправильно!",
                "restart": "Рестарт",
                "menu": "Главное меню",
                "play": "Играть",
                "settings": "Настройки",
                "exit": "Выход",
                "language": "Язык",
                "resolution": "Разрешение",
                "display_mode": "Режим экрана",
                "back": "Назад",
                "russian": "Русский",
                "ukrainian": "Украинский",
                "english": "Английский",
                "fullscreen": "Полноэкранный",
                "noframe": "Полноэкранный без рамки",
                "windowed": "Оконный",
                "colors": {
                    "red": "Красный",
                    "green": "Зеленый",
                    "blue": "Синий",
                    "yellow": "Желтый",
                    "purple": "Фиолетовый",
                    "black": "Черный"
                }
            },
            "ukrainian": {
                "start": "Натисніть будь-яку клавішу для початку",
                "avg_time": "Середній час: {avg_time:.2f} сек",
                "coefficient": "Коефіцієнт: {coefficient:.2f}",
                "accuracy": "Точність: {accuracy:.2f}%",
                "correct": "Правильно!",
                "incorrect": "Неправильно!",
                "restart": "Перезапуск",
                "menu": "Головне меню",
                "play": "Грати",
                "settings": "Налаштування",
                "exit": "Вихід",
                "language": "Мова",
                "resolution": "Роздільна здатність",
                "display_mode": "Режим екрана",
                "back": "Назад",
                "russian": "Російська",
                "ukrainian": "Українська",
                "english": "Англійська",
                "fullscreen": "Повноекранний",
                "noframe": "Повноекранний без рамки",
                "windowed": "Віконний",
                "colors": {
                    "red": "Червоний",
                    "green": "Зелений",
                    "blue": "Синій",
                    "yellow": "Жовтий",
                    "purple": "Фіолетовий",
                    "black": "Чорний"
                }
            }
        }
        self.set_language(language)

    def set_language(self, language):
        if language in self.translations:
            self.language = language

    def get_text(self, key):
        return self.translations[self.language].get(key, key)

    def get_color_name(self, color):
        return self.translations[self.language]["colors"].get(color, color)
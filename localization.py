from typing import Dict, Any, Tuple
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class ColorRGB:
    red: int
    green: int
    blue: int

    def to_tuple(self) -> Tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    @classmethod
    def from_tuple(cls, rgb: Tuple[int, int, int]) -> 'ColorRGB':
        return cls(rgb[0], rgb[1], rgb[2])

class LocalizationError(Exception):
    pass

class Localization:
    SUPPORTED_LANGUAGES = {"english", "russian", "ukrainian"}
    
    def __init__(self, language: str = "english"):
        self._colors: Dict[str, ColorRGB] = {
            "red": ColorRGB(255, 0, 0),
            "green": ColorRGB(0, 255, 0),
            "blue": ColorRGB(0, 0, 255),
            "yellow": ColorRGB(255, 255, 0),
            "purple": ColorRGB(128, 0, 128),
            "black": ColorRGB(0, 0, 0)
        }
        
        self._translations = self._load_translations()
        self.set_language(language)

    def _load_translations(self) -> Dict[str, Dict[str, Any]]:
        try:
            translations_path = Path("translations.json")
            if translations_path.exists():
                with open(translations_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load translations from file: {e}")
        
        return {
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

    def save_translations(self) -> None:
        try:
            with open("translations.json", "w", encoding="utf-8") as f:
                json.dump(self._translations, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Warning: Could not save translations to file: {e}")

    def set_language(self, language: str) -> None:
        if language not in self.SUPPORTED_LANGUAGES:
            raise LocalizationError(f"Language '{language}' is not supported. "
                                  f"Supported languages are: {', '.join(sorted(self.SUPPORTED_LANGUAGES))}")
        self._current_language = language

    @property
    def current_language(self) -> str:
        return self._current_language

    @property
    def colors(self) -> Dict[str, Tuple[int, int, int]]:
        return {name: color.to_tuple() for name, color in self._colors.items()}

    def get_text(self, key: str) -> str:
        try:
            return self._translations[self._current_language].get(key, key)
        except KeyError:
            print(f"Warning: Missing translation for key '{key}' in language '{self._current_language}'")
            return key

    def get_color_name(self, color: str) -> str:
        try:
            return self._translations[self._current_language]["colors"].get(color, color)
        except KeyError:
            print(f"Warning: Missing color translation for '{color}' in language '{self._current_language}'")
            return color

    def add_translation(self, language: str, translations: Dict[str, Any]) -> None:
        if not isinstance(translations, dict) or "colors" not in translations:
            raise LocalizationError("Translations must be a dictionary with 'colors' section")
        self._translations[language] = translations
        self.SUPPORTED_LANGUAGES.add(language)
        self.save_translations()

    def add_color(self, name: str, color: Tuple[int, int, int]) -> None:
        if not all(isinstance(v, int) and 0 <= v <= 255 for v in color):
            raise LocalizationError("Color values must be integers between 0 and 255")
            
        self._colors[name] = ColorRGB.from_tuple(color)
        
        for lang in self._translations:
            if "colors" not in self._translations[lang]:
                self._translations[lang]["colors"] = {}
            if name not in self._translations[lang]["colors"]:
                self._translations[lang]["colors"][name] = name
        
        self.save_translations()
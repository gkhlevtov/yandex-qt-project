import pytesseract  # 0.3.10
from cv2 import cv2  # opencv-python 4.5.4.58
from googletrans import Translator  # 4.0.0rc1

translator = Translator()  # Обозначаем переводчик
config = r'--oem 3 --psm 6 -l jpn'  # Задаём параметры перевода
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Указываем путь к tesseract
lang_dict = {"Русский": "ru",
             "Английский": "en",
             "Немецкий": "de",
             "Французский": "fr",
             "Итальянский": "it",
             "Испанский": "es",
             "Украинский": "uk",
             "Чешский": "cs",
             "Сербский": "sr",
             "Польский": "pl",
             "Корейский": "ko"}  # Словарь языковых обозначений


def translate(image_path, lang='en'):
    """Функция перевода текста"""

    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_text = pytesseract.image_to_string(img, config=config). \
        replace('\n', ''). \
        replace('.', '. '). \
        replace(' ', ''). \
        replace('', '')

    result = translator.translate(text=img_text, src='ja', dest='en')

    original_text = result.origin
    pronunciation_text = str(translator.translate(text=img_text, src='ja', dest='ja').pronunciation)

    if lang != 'en':
        result = translator.translate(result.text, src='en', dest=lang)

    return [original_text, pronunciation_text, result.text]

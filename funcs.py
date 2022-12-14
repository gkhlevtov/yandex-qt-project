import pytesseract  # 0.3.10
from googletrans import Translator  # 4.0.0rc1

translator = Translator()  # Обозначаем переводчик
config = r'--oem 3 --psm 6 -l jpn'  # Задаём параметры перевода
# Необходимо распаковать Tesseract-OCR.rar в директорию проекта
pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'  # Указываем путь к tesseract
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


def translate(image, lang='en'):
    """Функция перевода текста"""

    img_text = pytesseract.image_to_string(image, config=config). \
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

import random

def rewrite_text(text: str) -> str:
    """
    Простейший фейковый рерайт.
    Задача — слегка менять порядок слов и заменять синонимы.
    Это имитация рерайта без OpenAI API.
    """
    if not text:
        return ""

    # Разбиваем текст на предложения
    sentences = text.split(". ")

    rewritten = []
    for s in sentences:
        words = s.split()
        if len(words) > 4:
            random.shuffle(words)  # случайно перемешаем слова
        rewritten.append(" ".join(words))

    new_text = ". ".join(rewritten)

    return new_text + " (текст переработан автоматически)"

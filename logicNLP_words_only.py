import random
import re
import os

SENTENCE_PATTERN = None
ENDING_PATTERN = None

SENTENCE_ENDINGS = [
    '.', '?', '!'
]

SKIP_ABBREVIATIONS = None

# def split_sentences(text, isUsingExtraAbbr):
#     if not any(ending in text for ending in SENTENCE_ENDINGS):
#         return []
#     
#     raw_sentences = [m.group(1).strip() for m in SENTENCE_PATTERN.finditer(text)]
# 
#     sentences = []
#     buffer = ''
# 
#     for chunk in raw_sentences:
#         if not chunk.split():
#             continue
# 
#         chunk = chunk.strip()
#         if not ENDING_PATTERN.search(chunk):
#             chunk += '.'  # додай крапку, якщо немає завершення (для заголовків)
#         
#         if not isUsingExtraAbbr:
#             sentences.append(chunk)
#             continue
# 
#         # Якщо chunk — лише абревіатура або закінчується на неї — це не кінець
#         if isUsingExtraAbbr:
#             last_word = chunk.split()[-1] if chunk.split() else ''
#             if (chunk in SKIP_ABBREVIATIONS or any(last_word.endswith(abbr) for abbr in SKIP_ABBREVIATIONS)):
#                 buffer += chunk + ' '
#                 pass
#             else:
#                 full = (buffer + chunk).strip()
#                 if full:
#                     sentences.append(full)
#                 buffer = ''
#             pass
#         pass
# 
#     if isUsingExtraAbbr:
#         # Додаємо, якщо щось залишилось
#         if buffer.strip():
#             sentences.append(buffer.strip())
#             pass
# 
#     return sentences
# 
# def mixing_symbols_global(text, K, space=False):
#     """
#         Mixes symbols in the given text by swapping random pairs of characters.
# 
#         Args:
#             text (str): The input text to be modified.
#             K (int): The number of symbol mixings to perform.
#             space (bool, optional): Flag indicating whether to allow swapping spaces. Defaults to False.
# 
#         Returns:
#             str: The modified text with symbols mixed.
# 
#         Example:
#             text = "Hello, World!"
#             mixed_text = mixing_symbols_global(text, 5)
#             print(mixed_text)
#             leHlo, Wlord!
# 
#         """
#     text = text.replace(".", '')
#     text = list(text)
# 
#     for i in range(K):
#         while True:
#             x1, x2 = (random.randint(0, len(text) - 1), random.randint(0, len(text) - 1))
#             if space:
#                 break
#             if text[x1] != " " and text[x2] != " ":
#                 break
# 
#         text[x1], text[x2] = text[x2], text[x1]
#     return ''.join(text)
# 
# 
def mixing_words_global(text, K):
    """
    Mixes the words in the given text by swapping random pairs of words.

    Args:
        text (str): The input text to be modified.
        K (int): The number of word mixings to perform.

    Returns:
        str: The modified text with words mixed.

    Example:
        text = "Hello, world! This is a sample text."
        mixed_text = mixing_words_global(text, 3)
        print(mixed_text)
        world Hello This a is sample text

    """
    text = text.replace(".", '')
    text = text.split(" ")

    swap_indices = ((random.randint(0, len(text) - 1), random.randint(0, len(text) - 1)) for _ in range(K))
    for x1, x2 in swap_indices:
        text[x1], text[x2] = text[x2], text[x1]
    return ' '.join(text)


def mixing_strings_global(text, K, isUsingExtraAbbr):
    """
    Mixes substrings in the given text by swapping random pairs of substrings separated by periods.

    Args:
        text (str): The input text to be modified.
        K (int): The number of substring mixings to perform.

    Returns:
        str: The modified text with substrings mixed.

    Example:
        text = "Hello. World. This. Is. A. Test."
        mixed_text = mixing_strings_global(text, 3)
        print(mixed_text)
        This. World. Hello. Is. A. Test.

    """
    text = split_sentences(text, isUsingExtraAbbr)
    text_length = len(text)
    if text_length == 0:
        return ""
    swap_indices = ((random.randint(0, text_length-1), random.randint(0, text_length - 1)) for _ in range(K))
    for x1, x2 in swap_indices:
        text[x1], text[x2] = text[x2], text[x1]

    return ' '.join(text)


"""
Далі ф-ції для 2-локального перемішування
"""

# def lok2_mix_symbols_within_words(text, K, WIN, KROK):
#     text = text.replace(".", '')
#     text = text.split(" ")
#     text = [list(i) for i in text]
# 
#     for word in text:
#         if len(word) > 1:
#             swap_indexes = ((random.randint(0, len(word) - 1), random.randint(0, len(word) - 1)) for _ in range(K))
#             for x1, x2 in swap_indexes:
#                 word[x1], word[x2] = word[x2], word[x1]
# 
#     text = [''.join(i) for i in text]
# 
#     return ' '.join(text)
# 
# 
def lok2_mix_words_within_sentences(text, K, WIN, KROK, isUsingExtraAbbr):
    text = split_sentences(text, isUsingExtraAbbr)
    if text == "":
        return ""
    text = [i.split(' ') for i in text]

    for x in text:
        if len(x) > 1:
            swap_indexes = ((random.randint(0, len(x) - 1), random.randint(0, len(x) - 1)) for _ in range(K))
            for x1, x2 in swap_indexes:
                x[x1], x[x2] = x[x2], x[x1]

    text = [' '.join(i) for i in text]
    return ' '.join(text)


"""
Далі ф-ції для 1-локального пермішування
"""


# def lok1_mix_symbols_in_words(text, K, WIN, KROK):
#     text = list(text.replace(',', '').replace('.', ' '))
# 
#     for i in range(0, len(text), KROK):
#         for z in range(K):
#             for _ in range(7):
# 
#                 x1 = random.randint(i - WIN if i - WIN >= 0 else 0, i + WIN - 1 if WIN + i <= len(text) else len(text) - 1)
#                 x2 = random.randint(i - WIN if i - WIN >= 0 else 0, i + WIN - 1 if WIN + i <= len(text) else len(text) - 1)
# 
#                 if text[x1] != " " and text[x2] != " ":
#                     break
#             text[x1], text[x2] = text[x2], text[x1]
# 
#     return ''.join(text)
# 
# 
def lok1_mix_words_in_sentences(text, K, WIN, KROK):
    text = text.split(" ")

    for i in range(0, len(text), KROK):
        for y in range(K):
            for _ in range(7):

                x1 = random.randint(i - WIN if i - WIN >= 0 else 0, i + WIN - 1 if WIN + i <= len(text) else len(text) - 1)
                x2 = random.randint(i - WIN if i - WIN >= 0 else 0, i + WIN - 1 if WIN + i <= len(text) else len(text) - 1)
                if text[x1] != "." and text[x2] != ".":
                    break

            text[x1], text[x2] = text[x2], text[x1]

    return ' '.join(text)


# def lok1_mix_sentences_in_text(text, K, WIN, KROK, isUsingExtraAbbr):
#     """
#     Mixes the words in the given text by swapping random pairs of words.
# 
#     Args:
#         text (str): The input text to be modified.
#         K (int): The number of word mixings to perform.
# 
#     Returns:
#         str: The modified text with words mixed.
# 
#     Example:
#         text = "Hello, world! This is a sample text."
#         mixed_text = mixing_words_global(text, 3)
#         print(mixed_text)
#         world! Hello, This a is sample text.
# 
#     """
#     text = split_sentences(text, isUsingExtraAbbr)
#     if text == "":
#         return ""
#     
#     for i in range(0, len(text), KROK):
#         # for y in range(i-WIN,i+WIN):
#         swap_indexes = ((random.randint(i - WIN if i - WIN >= 0 else 0, i + WIN - 1 if WIN + i <= len(text) else len(text) - 1),
#                          random.randint(i - WIN if i - WIN >= 0 else 0, i + WIN - 1 if WIN + i <= len(text) else len(text) - 1)) for _ in range(K))
#         for x1, x2 in swap_indexes:
#             text[x1], text[x2] = text[x2], text[x1]
# 
#     return ' '.join(text)
# 
def load_list_from_file(file_path):
    items = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and line not in items:
                    items.append(line)
    return items

def init_sentence_pattern():
    
    global SKIP_ABBREVIATIONS
    global SENTENCE_ENDINGS

    abbreviations_file = 'abbreviations.txt'
    endings_file = 'endings.txt'

    extra_abbreviations = load_list_from_file(abbreviations_file)
    extra_endings = load_list_from_file(endings_file)

    print("default_endings : ", SENTENCE_ENDINGS, "\n")
    print("extra_endings (from endings.txt): ", extra_endings, "\n\n")
    print("extra_abbreviations (from abbreviations.txt): ", extra_abbreviations, "\n")

    SKIP_ABBREVIATIONS = list(extra_abbreviations)
    SENTENCE_ENDINGS = list(dict.fromkeys(SENTENCE_ENDINGS + extra_endings))

    ending_chars = ''.join(re.escape(c) for c in SENTENCE_ENDINGS)
    ending_pattern = f"[{ending_chars}]+|\\n{{2,}}"

    pattern = re.compile(rf"""
        (.*?                    
        (?:{ending_pattern}))
        (?=\s|$|\w|[^\x00-\x7F])
    """, re.VERBOSE | re.DOTALL)

    global SENTENCE_PATTERN
    SENTENCE_PATTERN = pattern

    global ENDING_PATTERN
    ENDING_PATTERN = re.compile(f"[{ending_chars}]+$")
    pass

if __name__ == "__main__":
    pass


from CodeTokenizer import CodeTokenizer

def process_code(code_text, file_name, shuffle=True):
    """
    Обробка комп'ютерного коду:
    - Токенізація коду
    - (Необов'язково) Перемішування токенів
    - Збір результату

    :param code_text: Рядок з кодом
    :param file_name: Ім'я файлу (для визначення мови)
    :param shuffle: Чи перемішувати токени
    :return: Перемішаний або оригінальний код (рядок)
    """
    tokenizer = CodeTokenizer(code_text, file_name)
    tokens = tokenizer.process()  # Отримуємо токени: [{'type': ..., 'value': ...}, ...]

    if shuffle:
        import random
        random.shuffle(tokens)  # Перемішуємо токени

    # Об'єднуємо значення токенів назад у рядок
    mixed_code = ''.join([token['value'] for token in tokens])

    return mixed_code
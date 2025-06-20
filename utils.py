import nltk
import ssl


def split_into_sentences(text):
    """
    Splits the given text into sentences.

    Args:
        text (str): The input text to be split into sentences.

    Returns:
        list: A list of sentences extracted from the text.

    Example:
        text = "Hello! How are you? I hope you're doing well."
        sentences = split_into_sentences(text)
        print(sentences)
        ['Hello!', 'How are you???', "I hope you're doing well."]

    """
    return nltk.sent_tokenize(text)


def download_nltk():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('punkt')


def get_all_words(text):
    """
    Retrieves all words from the given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of all words in the text.

    """
    tokens = nltk.word_tokenize(text)
    words = [word for word in tokens if word.isalpha()]
    # words = [token for token in tokens if token not in string.punctuation]
    return words


try:
    text = "Hello! How are you... I hope you're doing well."
    get_all_words(text)
except:
    download_nltk()

# nltk.download('popular')




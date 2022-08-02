import nltk
from nltk.corpus import stopwords
import spacy
from spacy.matcher import Matcher
import re

nltk.download('stopwords')

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def clean_the_text(text_reduced_spaces, txt):
    text_reduced_lines = re.sub(r'(\n\s*)+\n+', '\n', txt)
    clean_text = remove_emoji(text_reduced_spaces).lower()
    my_tokens = clean_text.split("\n")
    t = list(map(lambda x: x.strip(), my_tokens))
    my_words = []
    for i in t:
        if (i != '' and not re.match(r"(\(?)(\+?)(\d+)(\)?)(\s*)(\d+)(\s*)(\d+)(\s*)(\d+)(\s*)(\d+)", i)):
            my_words.append(i.split())
    words_here = [j for i in my_words for j in i]
    tokens_without_sw = [word for word in words_here if (
        not word in stopwords.words() and word != '•')]
    return tokens_without_sw




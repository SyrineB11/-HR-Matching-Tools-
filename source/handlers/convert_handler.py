from source.handlers.analyze_blocks import get_education_experience
from tika import parser
import re
import json
from source.handlers.clean_text import clean_the_text, remove_emoji
from source.handlers.extract_skills import get_skills
from source.handlers.extract_contact import get_contact
from source.handlers.extract_major_degrees import get_degrees, get_majors
from googletrans import Translator


"""def generate_N_grams(tokens_without_sw, ngram=1):
    temp = zip(*[tokens_without_sw[i:] for i in range(0, ngram)])
    ans = [' '.join(ngram) for ngram in temp]
    return ans"""


def get_text(resume):
    list_of_symbols_to_clean = ['(', ')', '[', ']', '•', ',']
    parsed_pdf = parser.from_file(resume, "http://apache-tika:9998")
    txt = parsed_pdf['content']
    ''.join(e for e in txt if e.isalnum())
    # Printing of content
    for symbol in list_of_symbols_to_clean:
        txt = txt.replace(symbol, "")
    text_reduced_lines = re.sub(r'(\n\s*)+\n+', '\n', txt)
    pattern = r'\.(\s*)\n'
    # Replace all occurrences of character s with an empty string
    text_reduced_spaces = re.sub(pattern, ' ', text_reduced_lines)
    clean_text = remove_emoji(text_reduced_spaces)
    tokens = clean_text.split("\n")
    (email, phone, github, linkedin) = get_contact(txt, tokens)
    """"    tokens_without_sw = clean_the_text(text_reduced_spaces, txt)
    list_of_grams = []
    for i in range(1, 3):
        list_of_grams.append(generate_N_grams(tokens_without_sw, i))
    grams_here = [j for i in list_of_grams for j in i]"""
    #old_code_hereeeeeeee
    translator = Translator()
    
    education_experience=get_education_experience(resume)
    return (email, phone, linkedin, github, get_skills(clean_text.replace("-", " ")), get_degrees(translator.translate(clean_text).text), get_majors(translator.translate(clean_text).text),education_experience[0],education_experience[1])

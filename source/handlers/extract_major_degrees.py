import spacy
from spacy import displacy
from googletrans import Translator

nlp_degrees = spacy.load("en_core_web_lg")
degrees_pattern_path = "degrees.jsonl"
ruler = nlp_degrees.add_pipe("entity_ruler")
ruler.from_disk(degrees_pattern_path)
nlp_degrees.pipe_names

nlp_majors = spacy.load("en_core_web_lg")
degrees_pattern_path = "majors.jsonl"
ruler = nlp_majors.add_pipe("entity_ruler")
ruler.from_disk(degrees_pattern_path)
nlp_majors.pipe_names


def get_degrees(text):
    translator = Translator()
    text = translator.translate(text)
    doc = nlp_degrees(text.text)
    print(doc)
    myset = []
    subset = []
    for ent in doc.ents:
        if "DEGREE" in ent.label_:
            subset.append(ent.label_.split('|')[1])
        myset.append(subset)
    return set(subset)


def get_majors(text):
    translator = Translator()
    text = translator.translate(text)
    doc = nlp_majors(text.text)
    print(doc)
    myset = []
    subset = []
    for ent in doc.ents:
        if "MAJOR" in ent.label_:
            subset.append(ent.text.lower())
        myset.append(subset)
    return set(subset)

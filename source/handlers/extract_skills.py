import spacy
from spacy import displacy
from source.handlers.clean_text import clean

nlp = spacy.load("en_core_web_lg")
skill_pattern_path = "data.jsonl"
ruler = nlp.add_pipe("entity_ruler")
ruler.from_disk(skill_pattern_path)
nlp.pipe_names


def get_skills(text):
    doc = nlp(clean(text))
    myset = []
    subset = []
    for ent in doc.ents:
        if "SKILL" in ent.label_:
            subset.append(ent.label_.split('|')[1])
        myset.append(subset)
    return set(subset)

import re
import numpy as np
from source.handlers.clean_text import clean_words
import unidecode


def detect_block(sorted_sth, pattern, page_index):
    for blockidx, block in enumerate(sorted_sth):
        sorted_lines = sorted(
            block["lines"], key=lambda x: x['bbox'][0], reverse=True)
        for lineidx, line in enumerate(sorted_lines):
            sorted_blocks = sorted(line["spans"], key=lambda x: x['bbox'][0])
            for wordidx, word in enumerate(sorted_blocks):
                if (re.search(pattern, clean_words(word['text'])) or re.search(pattern, unidecode.unidecode(word['text']))):
                    word["page"] = page_index
                    return(word)


def seperate_blocks(split_list, width):
    values = list(split_list.values())
    if ((abs(values[0]['bbox'][0]/2+values[0]['bbox'][2]/2-(values[1]['bbox'][0]/2+values[1]['bbox'][2]/2)) < 20 and values[1]['bbox'][0] > width/3)):
        return None
    for index in range(len(split_list)-1):
        if (abs(values[index]['bbox'][0]-values[index+1]['bbox'][0]) > 20):
            return values[index+1]['bbox'][0]

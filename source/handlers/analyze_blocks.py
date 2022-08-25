import re
from PyPDF2 import PdfFileReader
from source.handlers.extract_skills import get_skills
from source.handlers.extract_major_degrees import get_degrees
from source.handlers.handle_blocks import detect_block, seperate_blocks
from source.handlers.handle_dates import search_dates, detect_dates
import fitz
from source.models.resume import ExperienceModel, EducationModel

#This is a dictionary to detect the different blocks of a resume written in different forms
blocks_dict = {
    "experience": "^P(ROFESSIONAL|rofessional) E(xperience|XPERIENCE)(s|S)?(\s)*$|^E(xperience|XPERIENCE)(S|s)? (P|p)(ROFESSIONNELLE|rofessionnelles)(s|S)?(\s)*$|^E(xperience|XPERIENCE)(s|S)?(\s)*$|^R(ealisation|EALISATION)(s|S)?(\s)*$|^W(ORK|ork) (E|e)(xperience|XPERIENCE)(s|S)?(\s)*$|^W(ork|ORK) (H|h)(istory|ISTORY)(\s)*$|I(NTERNERSHIP|nternership)(s|S)?(\s)*",
    "education": "^E(ducation|DUCATION)(\s)*$|^F(ORMATION|ormation)(\s)*$",
    "skills": "^S(kills|KILLS)(\s)*$|^C(ompetences|OMPETENCES)(\s)*$|^T(echnical|ECHNICAL) (S|s)(kills|KILLS)(\s)*$|^E(XPERTISE|xpertise)(\s)*$",
    "contact": "^C(ontact|ONTACT)(\s)*$|C(oordonnees|OORDONNEES)(\s)*$|C(ONTACT|ontact) (M|m)(e|E) (A|a)(T|t)(\s)*$",
    "languages": "^L(ANGUES|angues)(\s)*$|^L(ANGUAGES|anguages)(\s)*$|^L(ANGAGES|angages)(\s)*$",
    "projects": "^P(rojects|ROJECTS)(\s)*$|^P(ERSONAL|ersonal) (P|p)(ROJECTS|rojects)(\s)*$|^P(rojets|ROJETS)( (P|p)(ERSONNELS|ersonnels))?(\s)*$",
    "course": "^C(OURSE|ourse)s?(\s)*$",
    "certificates": "^C(ERTIFICATES,ertificates)(\s)*$|^C(ERTIFICATIONS|ertifications)(\s)*$|^C(ERTIFICATS|ertificats)(\s)*$|^C(ERTIFICATS|ertificats) (O|o)(BTENUS|btenus)(\s)*$|^A(ttestations|TTESTATIONS)(\s)*$",
    "community_life": "^C(OMMUNITY|ommunity) E(NGAGEMENT|ngagement)(\s)*|^C(OMMUNITY|ommunity) (L|l)(IFE|ife)(\s)*$|^S(OCIAL|ocial) (L|l)(IFE|ife)(\s)*$|^V(ie|IE) (S|s)(ociale|OCIALE)(\s)*$|^V(IE|ie) (A|a)(ssociative|SSOCIATIVE)(\s)*$|^E(XPERIENCES|xperiences) (E|e)(XTRA-SCOLAIRES|xtra-scolaires)(\s)*$|^C(OMMUNITY|ommunity) (W|w)(ORK|ork)(s|S)?(\s)*$",
    "recommendations": "^R(ECOMMANDATIONS|ecommandations)(\s)*$|^R(ecommendations|ECOMMENDATIONS)(\s)*",
    "interests": "^I(NTERESTS|nterests)(\s)*$|^I(NTERETS|nterets)(\s)*$|^C(ENTRES|entres) (D|d)'(I|i)(NTERET|nteret)(\s)*$|^I(NTERET|interet)(\s)*$"
}


def analyze_block(page_detected, block_limiter, selected_block, right_block, vertical_resume, block_to_analyze):
    block_string = ''
    array_block = []
    index = list(selected_block.keys()).index(block_to_analyze)
    blocks = page_detected.get_text('dict', flags=0)['blocks']
    sorted_page_blocks = sorted(blocks, key=lambda x: x['bbox'][1])
    for blockidx, block in enumerate(sorted_page_blocks):
        verical_delimiter = vertical_delimiter = block['bbox'][1] < list(
            selected_block.values())[index+1]['bbox'][1] if index < len(selected_block)-1 else True
        if ((vertical_resume or (not right_block and block['bbox'][2] < block_limiter) or (right_block and block['bbox'][0] > block_limiter)) and block['bbox'][1] >= selected_block[block_to_analyze]['bbox'][1] and vertical_delimiter):
            sorted_lines = sorted(
                block["lines"], key=lambda x: x['bbox'][0], reverse=True)
            for lineidx, line in enumerate(sorted_lines):
                sorted_blocks = sorted(
                    line["spans"], key=lambda x: x['bbox'][0])
                for wordidx, word in enumerate(sorted_blocks):
                    block_string = "\n".join([block_string, word['text']])

    (extracted_dates, blocks) = search_dates(block_string)
    print("my blockssss=========",blocks)
    for date in extracted_dates:
        start_date, end_date = detect_dates(date)
        array_block.append({"start_date": start_date, "end_date": end_date})
    if (block_to_analyze == "education"):
        degrees = []
        for index in range(len(blocks)):
            degrees.append(get_degrees(blocks[index]))
        degrees = degrees[1:] if len(
            degrees[-1]) != 0 else degrees[:len(degrees)-1]
        education_list = []
        for index in range(len(degrees)):
            education_list.append(EducationModel(
                start_date=array_block[index]['start_date'], end_date=array_block[index]['end_date'], degrees=degrees[index]))
        return(education_list)
    else:
        experience_list = []
        for index in range(1, len(extracted_dates)+1):
            experience_list.append(ExperienceModel(
                start_date=array_block[index-1]['start_date'], end_date=array_block[index-1]['end_date'], skills=get_skills(blocks[index])))
        return(experience_list)


def find_block(block_to_detect, list_of_blocks):
    for index, block in enumerate(list_of_blocks):
        if block_to_detect in block:
            return index, block
    return None,None


def analyze_education_experience(index, split_page_blocks, fitzdoc, block_to_analyze):
    if (index != None):
        left_blocks_sorted = []
        right_blocks_sorted = []
        for page in range(len(fitzdoc)):
            for split_blocks in split_page_blocks:
                left_blocks = {}
                right_blocks = {}
                sorted_blocks = dict(sorted(
                    list(split_blocks.items()), key=lambda x: x[1]['bbox'][0], reverse=False))
                for iterate_blocks in sorted_blocks:
                    if sorted_blocks[iterate_blocks]['bbox'][2] < index and sorted_blocks[iterate_blocks]["page"] == page:
                        left_blocks.update(
                            {iterate_blocks: sorted_blocks[iterate_blocks]})
                    elif(sorted_blocks[iterate_blocks]["page"] == page):
                        right_blocks.update(
                            {iterate_blocks: sorted_blocks[iterate_blocks]})
                left_blocks_sorted.append(dict(sorted(
                    list(left_blocks.items()), key=lambda x: x[1]['bbox'][1], reverse=False)))
                right_blocks_sorted.append(dict(sorted(
                    list(right_blocks.items()), key=lambda x: x[1]['bbox'][1], reverse=False)))
        left_block_x1 = list(left_blocks_sorted[0].values())[0]['bbox'][2]
        right_block_x0 = list(right_blocks_sorted[0].values())[0]['bbox'][0]
        index, detected_block = find_block(
            block_to_analyze, right_blocks_sorted)
        if (detected_block != None):
            return analyze_block(fitzdoc[right_blocks_sorted[index][block_to_analyze]["page"]],
                          left_block_x1, detected_block, True, False, block_to_analyze)
        else:
            index, detected_block = find_block(
                block_to_analyze, left_blocks_sorted)
            return analyze_block(fitzdoc[left_blocks_sorted[index][block_to_analyze]["page"]],
                          right_block_x0, detected_block, False, False, block_to_analyze)
    else:
        vertical_blocks_sorted = []
        for page_block in split_page_blocks:
            vertical_blocks_sorted.append(
                dict(sorted(page_block.items(), key=lambda x: x[1]['bbox'][1], reverse=False)))
        index, detected_block = (find_block(
            block_to_analyze, vertical_blocks_sorted))
        return analyze_block(fitzdoc[vertical_blocks_sorted[index][block_to_analyze]
                      ["page"]], None, detected_block, False, True, block_to_analyze)


def get_education_experience(file):
    fitzdoc = fitz.open(file)
    resume_blocks = {}
    for page_index in range(len(fitzdoc)):
        blocks = fitzdoc[page_index].get_text('dict', flags=0)['blocks']
        sorted_page_blocks = sorted(blocks, key=lambda x: x['bbox'][1])
        for key, value in blocks_dict.items():
            block = detect_block(sorted_page_blocks, value, page_index)
            if (block):
                resume_blocks.update({key: block})
    keys_list = list(resume_blocks.keys())
    values_list = list(resume_blocks.values())
    split_page_blocks = [{keys_list[0]:values_list[0]}]
    index = 0
    for resume_keys in range(1, len(keys_list)):
        if (values_list[resume_keys]["page"] != values_list[resume_keys-1]["page"]):
            index = index+1
            split_page_blocks.append(
                {keys_list[resume_keys]: values_list[resume_keys]})
        else:
            split_page_blocks[index].update(
                {keys_list[resume_keys]: values_list[resume_keys]})
    split_list = dict(sorted(split_page_blocks[0].items(
    ), key=lambda x: x[1]['bbox'][0]), reverse=False)
    index = seperate_blocks(split_list, fitzdoc[0].rect.width)
    pattern_to_search = ["education", "experience"]
    result_blocks = []
    for pattern in pattern_to_search:
        result_blocks.append(analyze_education_experience(index, split_page_blocks, fitzdoc, pattern))
    return result_blocks

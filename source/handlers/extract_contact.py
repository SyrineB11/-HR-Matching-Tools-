import re


def get_contact(txt, tokens):
    email = re.findall("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", txt)
    linkedin = None
    for t in tokens:
        match = re.match(
            r"http(s)?:\/\/([w]{3}\.)?linkedin\.com\/in\/[\w+-]{5,20}\/?|linkedin\/[\w+-]{5,20}|linkedin\.com\/in\/[\w+-]{5,20}\/?", t.lower())
        if (match):
            linkedin = t[match.start():match.end()]
    github = None
    for t in tokens:
        match = re.match(r"(https:\/\/)?github\.com/(\w+)", t)
        if (match):
            github = t[match.start():match.end()]
    phone = None
    for t in tokens:
        match = re.match(
            r"(\(?)(\+?)(\d+)(\)?)(\s*)(\d+)(\s*)(\d+)(\s*)(\d+)(\s*)(\d+)", t)
        if (match):
            phone = t[match.start():match.end()]
    return (email[0], phone, github, linkedin)

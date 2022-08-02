import re

patterns_dict = {
    "email": "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "linkedin": r"http(s)?:\/\/([w]{3}\.)?linkedin\.com\/in\/[\w+-]{5,20}\/?|linkedin\/[\w+-]{5,20}|linkedin\.com\/in\/[\w+-]{5,20}\/?",
    "github": r"(https:\/\/)?github\.com/(\w+)",
    "phone": r"(\(?)(\+?)(\d+)(\)?)(\s*)(\d+)(\s*)(\d+)(\s*)(\d+)(\s*)(\d+)"
    
}


def get_contact(txt, tokens):
    email = re.findall(patterns_dict["email"], txt)
    linkedin = None
    for t in tokens:
        match = re.search(
            patterns_dict["linkedin"], t.lower())
        if (match):
            linkedin = t[match.start():match.end()]
    github = None
    for t in tokens:
        match = re.search(patterns_dict["github"], t)
        if (match):
            github = t[match.start():match.end()]
    phone = None
    for t in tokens:
        match = re.match(patterns_dict["phone"]
            , t)
        if (match):
            phone = t[match.start():match.end()]
    return (email[0], phone, github, linkedin)

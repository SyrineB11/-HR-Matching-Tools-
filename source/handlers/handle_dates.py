import datetime
import re
from googletrans import Translator
month_dict = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
    "jan": 1,
    "feb": 2,
    "aug": 8,
    "sept": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12
}
months = "(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|aug|sept|oct|nov|dec|0[1-9]|1[0-2])"
months_present = "(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|aug|sept|oct|nov|dec|[0-9]{4}|0[1-9]|1[0-2]|present)"
months_with_letters = "(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|aug|sept|oct|nov|dec)"
date_pattern = "(?:\(|\n)(?:\s|,)*"+months+"(?:\s)*/(?:\s)*[0-9]{4}(?:\s)*(?:-|–)(?:\s)*"+months_present+"(?:\s)*(?:/(?:\s)*[0-9]{4})?|(?:\n|\(|\||,)(?:\s)*"+months+"(?:\s)*(?:\n)?(?:\s)*[0-9]{4}(?:\s)*(?:\n)?(?:-|–)(?:\s)*(?:\n)?(?:\s)*"+months_present+"(?:\s)*(?:\n)?(?:\s)*(?:[0-9]{4})?|(?:\n|\(|\||,)(?:\s)*" + \
    months+"(?:\s)*/?(?:\s)*(?:[0-9]{4}|[0-9]{2})|\n(?:\s)*"+months+"(?:\s)*(?:-|–)(?:\s)*"+months + \
    "(?:\s)*/?(?:\s)*(?:[0-9]{4}|[0-9]{2})|(?:\||\n|,)(?:\s)*[0-9]{4}(?:\s)*(?:-|–)(?:\s)*(?:[0-9]{4}|present)|(?:\||\n)(?:\s)*[0-9]{4}|\((?:\s)*"+months+"(?:\s)*[0-9]{4}"


def detect_dates(date):
    split_dates = date.split(" ")
    if re.match("(?:0[1-9]|1[0-2]) [0-9]{4} (?:-|–) (?:0[1-9]|1[0-2]) [0-9]{4}", date):
        return format_date(int(split_dates[1]), int(split_dates[4]), int(split_dates[0]), int(split_dates[3]))
    elif re.match(months_with_letters+" [0-9]{4} (?:-|–) "+months_with_letters+" [0-9]{4}", date):
        return format_date(int(split_dates[1]), int(split_dates[4]), month_dict[split_dates[0]], month_dict[split_dates[3]])
    elif re.match("(?:0[1-9]|1[0-2]) [0-9]{4} (?:-|–) present", date):
        start_date = str(datetime.datetime(
            int(split_dates[1]), int(split_dates[0]), 1))
        end_date = str(datetime.datetime.now())
        return (start_date, end_date)
    elif re.match(months_with_letters+" [0-9]{4} (?:-|–) present", date):
        start_date = str(datetime.datetime(
            int(split_dates[1]), month_dict[split_dates[0]], 1))
        end_date = str(datetime.datetime.now())
        return(start_date, end_date)
    elif re.match("(?:0[1-9]|1[0-2])"+" [0-9]{4} (?:-|–) [0-9]{4}", date):
        return format_date(int(split_dates[1]), int(split_dates[3]), int(split_dates[0]), int(split_dates[0]))
    elif re.match(months_with_letters+" [0-9]{4} (?:-|–) [0-9]{4}", date):
        return format_date(int(split_dates[1]), int(split_dates[3]), month_dict[split_dates[0]], month_dict[split_dates[0]])
    elif re.match(months_with_letters+" (?:-|–) "+months_with_letters+" [0-9]{4}", date):
        return format_date(int(split_dates[3]), int(split_dates[3]), month_dict[split_dates[0]], month_dict[split_dates[2]])
    elif re.match("(?:0[1-9]|1[0-2]) (?:-|–) (?:0[1-9]|1[0-2]) [0-9]{4}", date):
        return format_date(int(split_dates[3]), int(split_dates[3]), int(split_dates[0]), int(split_dates[2]))
    elif re.match("(?:0[1-9]|1[0-2]) (?:-|–) (?:0[1-9]|1[0-2]) [0-9]{2}", date):
        year = int('20'+split_dates[3]) if int(split_dates[3]
                                               ) < 50 else int('19'+split_dates[3])
        return format_date(year, year, int(split_dates[0]), int(split_dates[2]))
    elif re.match(months_with_letters+" (?:-|–) "+months_with_letters+" [0-9]{2}", date):
        year = int('20'+split_dates[3]) if int(split_dates[3]
                                               ) < 50 else int('19'+split_dates[3])
        return format_date(year, year, month_dict[split_dates[0]], month_dict[split_dates[2]])
    elif re.match("(?:0[1-9]|1[0-2]) [0-9]{4}", date):
        return format_date(int(split_dates[1]), int(split_dates[1]), int(split_dates[0]), int(split_dates[0]))
    elif re.match(months_with_letters+" [0-9]{4}", date):
        return format_date(int(split_dates[1]), int(split_dates[1]), month_dict[split_dates[0]], month_dict[split_dates[0]])
    elif re.match(months_with_letters+" (?:[5-9][0-9]|[0-7][0-9])", date):
        year = int('20'+split_dates[1]) if int(split_dates[1]
                                               ) < 50 else int('19'+split_dates[1])
        return format_date(year, year, month_dict[split_dates[0]], month_dict[split_dates[0]])
    elif re.match("(?:0[1-9]|1[0-2]) (?:[5-9][0-9]|[0-7][0-9])", date):
        year = int('20'+split_dates[1]) if int(split_dates[1]
                                               ) < 50 else int('19'+split_dates[1])
        return format_date(year, year, int(split_dates[0]), int(split_dates[0]))
    elif re.match("[0-9]{4} (?:-|–) [0-9]{4}", date):
        return format_date(int(split_dates[0]), int(split_dates[2]), 1, 12)
    elif re.match("[0-9]{4} (?:-|–) present", date):
        start_date = str(datetime.datetime(int(split_dates[0]), 1, 1))
        end_date = str(datetime.datetime.now())
        return (start_date, end_date)
    elif re.match("[0-9]{4}", date):
        return format_date(int(date), int(date), 1, 12)


def format_date(start_year, end_year, start_month, end_month):
    start_date = str(datetime.datetime(start_year, start_month, 1))
    end_date = str(datetime.datetime(end_year, end_month, 28))
    return(start_date, end_date)


def search_dates(block_string):
    translator = Translator()
    text = translator.translate(block_string)
    find_all_result = re.findall(date_pattern, text.text.lower())
    dates = " ".join(find_all_result)
    dates = dates.replace("/", " ")
    dates = dates.replace("\n", " ")
    dates = dates.replace("-", " - ")
    dates = dates.replace("–", " – ")
    result = re.sub(' +', ' ', dates)

    find_all_result = re.findall(months+" [0-9]{4} (?:-|–) "+months+" [0-9]{4}|"+months+" [0-9]{4} (?:-|–) present|"+months+" [0-9]{4} (?:-|–) [0-9]{4}|"+months+" (?:-|–) " +
                                 months+" (?:[0-9]{4}|[0-9]{2})|"+months+" [0-9]{4}|"+months+" (?:[5-9][0-9]|[0-7][0-9])|[0-9]{4} (?:-|–) (?:present|[0-9]{4})|[0-9]{4}", result)
    return (find_all_result, re.split(date_pattern, text.text.lower()))

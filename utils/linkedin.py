import re

def validateLinkedInURL(url):
    pattern = r"^https:\/\/(www\.)?linkedin\.com\/.*$"
    return bool(re.match(pattern, url))

def notURL(text):
    pattern = re.compile(
        r'^(https?:\/\/)?'
        r'(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}|localhost|(\d{1,3}\.){3}\d{1,3})'
        r'(:\d+)?(\/[^\s]*)?$'
    )
    return not bool(pattern.match(text))

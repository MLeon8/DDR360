# preprocess.py



import re


def preprocess_text(text):
    if isinstance(text, str):  
        text = text.lower()
        text = re.sub(r'\d+', '', text)  
        text = re.sub(r'[^\w\s]', '', text)  
        text = text.strip()
        return text
    else:
        return ''

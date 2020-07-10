import json
from fuzzywuzzy import fuzz

def confidenceCheck(title):
    # getting the keywords to find
    keywords = json.load(open('core/titleKeys.json', 'r'))['keywords']

    # looping through the keywords and checking its confidence
    confidences = [fuzz.ratio(title.lower(), key.lower()) for key in keywords]

    return max(confidences)

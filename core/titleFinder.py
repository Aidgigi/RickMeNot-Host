import json
from fuzzywuzzy import fuzz

def confidenceCheck(title):

    # getting the keywords to find
    keywords = json.load(open('core/titleKeys.json', 'r'))['keywords']

    # making a list for the possible confidences
    confidences = []

    # looping through the keywords, checking its confidence, and appening it to the list
    for key in keywords:
        confidences.append(fuzz.ratio(title.lower(), key.lower()))

    return max(confidences)

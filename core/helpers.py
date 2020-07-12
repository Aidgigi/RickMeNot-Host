from collections import Counter

# a function to return all unique values from a list
def unique(list1):

    # insert the list to the set
    listSet = set(list1)
    # convert the set to the list
    return (list(listSet))


# this function takes a list, and a value, and counts the value's occurance in a list
def countOcc(data, value):

    #creating a dict to work with
    occDict = {}

    for x in value:
        occDict[x] = data.count(x)

    return occDict


# this function takes a dict and returns a sorted version
def dictSort(data):

    #magical lambda fuckery
    return {k: v for k, v in sorted(data.items(), key = lambda item: item[1], reverse = True)}


def dictMerge(dict1, dict2):

    dictA = Counter(dict1)
    dictB = Counter(dict2)

    return dict(dictA + dictB)

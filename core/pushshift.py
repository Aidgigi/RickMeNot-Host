import requests

def getComments(limit, after):

    url = f"https://api.pushshift.io/reddit/search/comment?after={after}&?limit={limit}"
    #params = {"limit": str(limit), "after": str(after)}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

    try:
        response = requests.get(url, headers = headers)

    except Exception as e:
        print(f"[PUSHSHIFT] Error! {e}!")
        return False

    # error handling
    response.raise_for_status()
    jsonData = response.json()

    if 'data' in jsonData:

        # blank list for holding comments
        comments = []

        for comment in jsonData['data']:
            print(comment['body']+'\n')
            comments.append(comment['id'])

        return len(comments)


    else:
        print("[PUSHSHIFT] Warning! Bad Data!")
        return False

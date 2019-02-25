import requests
import json
from threading import Thread

def execute_query(query, threaded=False, debug=False):
    if threaded:
        return Thread(target=execute_query, args=[query]).start()
    if debug:
        print(query)

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = 'http://68.183.133.221/mundim/execute.php' if 'insert' in query.lower() else 'http://68.183.133.221/mundim/query.php'
    content = ''
    try:
        response = requests.post(url, headers=headers, data={'query': query})
        if debug:
            print response, response.content
        content = response.content
    except:
        print '** execute_query failed **'

    return content

def load_query(query, debug=False):
    load = None
    try:
        load = json.loads(execute_query(query, debug=debug))
    except:
        print '** json loads failed **'
    return load

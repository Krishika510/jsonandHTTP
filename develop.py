import requests

AUTH = {'userKey': '95fc6b26d76e80d1c01bd9c43c7c'}
COMMON_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/'
GET_URL = 'dataset'
POST_URL = 'result'


def convertTimeToMinutes(millis_1):
    if millis_1 <= 600000:
        return True
    else:
        return False

def convertData(data):
    result = {}
    data['events'].sort(key=lambda x: x['timestamp'])
    for cur in data['events']:
        time = cur['timestamp']
        visitorId = cur['visitorId']
        page = cur['url']

        insert = False
        if visitorId not in result:
            result[visitorId] = [{'duration': 0, 'pages': [page], 'startTime': time, 'latestTime': time}]
        else:
            for key, value in result.items():
                if key == visitorId:
                    for i in range(len(value)):
                        if convertTimeToMinutes(time - value[i]['latestTime']) <= 10:
                            insert = True
                            value[i]['duration'] = time - value[i]['startTime']
                            value[i]['pages'].append(page)
                            value[i]['latestTime'] = time
                            value[i]['pages'].sort()

                    if not insert:
                        result[visitorId].append({'duration': 0, 'pages': [page], 'startTime': time, 'latestTime': time})

    for key, value in result.items():
        value.sort(key=lambda x: x['startTime'])
        for i in range(len(value)):
            del value[i]['latestTime']

    final_result = {'sessionsByUser': result}
    print(final_result)
    return final_result


def getMethod():
    r = requests.get(COMMON_URL+GET_URL, params=AUTH)
    output = convertData(r.json())
    return output


def postMethod(output):
    headers = {
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }
    r = requests.post(COMMON_URL+POST_URL, params=AUTH,
                      json=output, headers=headers)


if __name__ == '__main__':
    data = getMethod()
    postMethod(data)

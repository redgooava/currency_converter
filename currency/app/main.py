import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse


def get_data():
    access_key = 'c6748d763854a42ddfffa6ef5f528d47'

    params = {
        'access_key': access_key
    }

    req = requests.get('http://data.fixer.io/api/latest', params=params)
    result = req.json()['rates']
    result['EUR'] = 1
    return result


app = FastAPI()


@app.get('/api/rates')
def main(_from: str, _to: str, _value: int):
    data = get_data()
    if _from not in data:
        return JSONResponse(content={'message': 'Incorrect first currency (_from)'}, status_code=400)
    if _to not in data:
        return JSONResponse(content={'message': 'Incorrect second currency (_to)'}, status_code=400)
    if not isinstance(_value, int) or _value < 0:
        return JSONResponse(content={'message': 'Incorrect value (_value)'}, status_code=400)
    return JSONResponse(content={'result': data[_from] * _value / data[_to]}, status_code=200)

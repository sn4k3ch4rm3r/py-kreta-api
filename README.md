# Python wrapper for e-Kreta API v3

## Installation
```
pip install git+https://github.com/sn4k3ch4rm3r/py-kreta-api/
```
or
```sh
git clone https://github.com/sn4k3ch4rm3r/py-kreta-api/
cd py-kreta-api
python setup.py install
```

## Example
```py
from kreta_api import KretaAPI

api = KretaAPI("user agent")

api.authenticate("username", "password", "institute_id")
api.get_timetable("2021-03-01", "2021-03-07")
```

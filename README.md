# Репозиторий с домашним заданием по основам backend

Реализованы два handler-а.
1. readPlateImage - определяет номер с картинки, картинка задается id из определенного пула.
Route - BASE_URL/readPlateImage/<id>
2. readPlateImages - делает все тоже что и первый, но можно подать на вход несколько id, используя HTTP-запрос. Например, можно использовать следующий код:
```python
import requests

data = {'ids' : ['10022','9965']}
r = requests.post('BASE_URL/readPlateImages',
                  json=data)
print(r.json())
```

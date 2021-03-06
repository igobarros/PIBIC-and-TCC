## Projeto

### Como rodar o projeto
```bash
$ git clone https://github.com/IgoPereiraBarros/PIBIC-and-TCC.git
$ cd projeto
$ python3 -m venv .venv
$ pip install -r requirements.txt
```

### Configurando

Antes de executar o script ```build_model.py``` precisamos alterar as credenciais do banco de dados usando às suas, na raiz do projeto no arquivo ```settings.py```:
```py
CONFIG_DEV = {
	'MONGO_URI': 'mongodb://user:password@localhost:27017/admin',
	'MONGO_DBNAME': 'DBNAME',
	'COLLECTION_NAME': 'COLLECTION_NAME'
}
```
OBS: Use as mesmas credenciais, banco e collection usado no projeto da pasta ```crawler.```

### Executando o projeto

- Crie duas pastas na raiz do projeto, ```models_pkl``` e ```vectorizers_pkl.```
- Execute o script ```python3 build_model.py```, após concluído rode a API ```python3 api.py```

### Testando a aplicação

GET
```py
import requests

url = 'http://localhost:5000/predict'
params = {'query': 'A aplicação deverá delinear o perfil político do candidato, destacando sua área de atuação, para isso deve relacionar os posts rastreados com uma ou mais áreas de atuação específica (saúde, educação, segurança pública).'}
response = requests.get(url, params)
print(response.json())
```
Rode esse script para fazer uma requisão GET à API.

### Usando o postman
**GET**

![get](https://user-images.githubusercontent.com/34240682/71228271-775efb00-22c0-11ea-814e-e446f0103477.png)

**POST**

![post](https://user-images.githubusercontent.com/34240682/71228306-88a80780-22c0-11ea-95bb-69c0bca48073.png)

### Contados
* E-mail: igorestacioceut@gmail.com
* Linkendin: [Igo Pereira Barros](https://www.linkedin.com/in/igo-pereira-barros-developer/)
* Instagram: [igor.p.barros](https://www.instagram.com/igor.p.barros/)
* Telegram: @IgoBarros

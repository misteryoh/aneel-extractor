import requests
import polars as pl
import re

class RequestsApi:

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.session = requests.Session()

    def get_api_data(self, url, enpoint):

        response = self.session.get(url+enpoint)

        # Inicializa lista dos resultados
        keep_loop = True
        data = []

        while keep_loop:

            # Verifica se a requisição foi bem sucedida
            if response.status_code == 200:
                keep_loop = True
            else:
                print('Erro ao acessar a API')

            # Arquivo JSON retornado pela API
            content = response.json()['result']

            # Loop na lista para extrair os IDs e URIs das proposições e retorna um dicionário
            data.extend(content['records'])

            # Verifica quantidade de paginas para consulta
            check_next = content['_links']

            try:
                next_api = check_next.get('next')
            except:
                print("Deu ruim")

            match = re.search(r'offset=(\d+)', next_api)

            if match:
                offset_number = int(match.group(1))

            if next_api is not None and offset_number < content['total']:
                response = requests.get(url+next_api)
                print(next_api)
                keep_loop = True
            else:
                keep_loop = False

        df = pl.DataFrame(data=data)

        return df


import requests
import pandas as pd
import re
from pyspark.sql import SparkSession

url = "https://dadosabertos.aneel.gov.br"
api = "/api/3/action/datastore_search?resource_id=11ec447d-698d-4ab8-977f-b424d5deee6a"
#api_cadastro = "/api/3/action/datastore_search?resource_id=20ef769f-a072-489d-9df4-c834529f8a78"

response = requests.get(url+api)

# Inicializa lista dos resultados
keep_loop = True
data = []

spark = SparkSession.builder.appName("Aneel-Siga").getOrCreate()

schema = """
_id INT,
DatGeracaoConjuntoDados STRING,
NomEmpreendimento STRING,
IdeNucleoCEG STRING,
CodCEG STRING,
SigUFPrincipal STRING,
SigTipoGeracao STRING,
DscFaseUsina STRING,
DscOrigemCombustivel STRING,
DscFonteCombustivel STRING,
DscTipoOutorga STRING,
NomFonteCombustivel STRING,
DatEntradaOperacao STRING,
MdaPotenciaOutorgadaKw STRING,
MdaPotenciaFiscalizadaKw STRING,
MdaGarantiaFisicaKw STRING,
IdcGeracaoQualificada STRING,
NumCoordNEmpreendimento STRING,
NumCoordEEmpreendimento STRING,
DatInicioVigencia STRING,
DatFimVigencia STRING,
DscPropriRegimePariticipacao STRING,
DscSubBacia STRING,
DscMuninicpios STRING
"""

df_siga = spark.createDataFrame([], schema)

while keep_loop:

    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        keep_loop = True
    else:
        print('Erro ao acessar a API')

    # Arquivo JSON retornado pela API
    content = response.json()['result']

    rdd = spark.sparkContext.parallelize(response.json()['result'])
    df = rdd.toDF(schema)

    df_siga.union(df)

    # Loop na lista para extrair os IDs e URIs das proposições e retorna um dicionário
    for item in content['records']:
        
        data.append(item)

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
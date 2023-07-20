import requests
import polars as pl
import re
from src.RequestsController import RequestsApi

url = "https://dadosabertos.aneel.gov.br"
api_ceg = "/api/3/action/datastore_search?resource_id=11ec447d-698d-4ab8-977f-b424d5deee6a"
api_agente = "/api/3/action/datastore_search?resource_id=20ef769f-a072-489d-9df4-c834529f8a78"

request_api = RequestsApi()

df_ceg = request_api.get_api_data(url, api_ceg)
df_agente = request_api.get_api_data(url, api_agente)

print(df_ceg)
print(df_agente)


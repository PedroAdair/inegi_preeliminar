import requests
import pandas as pd


def consultaTotalBilletesMonedas(key: str, infoConsultas:dict, config:dict):
    consulta = infoConsultas[key]
    consultarHistoricos = "/datos/?"
    use_token = f"token={config['BM_token']}"
    url = consulta + consultarHistoricos + use_token
    try:
        respuesta = requests.get(url).json()
        title = respuesta["bmx"]["series"][0]["titulo"]
        data = respuesta["bmx"]["series"][0]["datos"]
        df_query = pd.DataFrame(data)
        df_query.fecha  = pd.to_datetime(df_query.fecha, format="%d/%m/%Y")
        df_query = df_query.set_index("fecha")
        df_query["dato"] = df_query["dato"].str.replace(',', '', regex=False)
        df_query['dato'] = df_query['dato'].astype(float)
        df_query = df_query.rename(columns={"dato": " ".join(title.split(" ")[-2:]) })
        return title, df_query
    except Exception as e:
        None
        return "Inconsistencia al obtener la consulta", pd.DataFrame()
    
def INPC_historico(inflacionHistorica:dict,
                   Periodo:str,
              min_date = str):
    InflacionHistoricaQ = inflacionHistorica[Periodo]
    respuesta = requests.get(url=InflacionHistoricaQ).json()
    data = respuesta["Series"][0]["OBSERVATIONS"]
    df_inflacion = pd.DataFrame(data=data)
    df_inflacion["TIME_PERIOD"]  = pd.to_datetime(df_inflacion["TIME_PERIOD"], format="%Y/%m")
    df_inflacion.OBS_VALUE = df_inflacion.OBS_VALUE.replace({"": "0"}).astype(float)
    df_inflacionPeriodo = df_inflacion.set_index("TIME_PERIOD")[["OBS_VALUE"]].sort_index().rename(columns={"OBS_VALUE": f"Inflacion_{Periodo}"})
    df_inflacionPeriodo = df_inflacionPeriodo[df_inflacionPeriodo.index >= pd.to_datetime(min_date, format = "%d-%m-%Y")]
    return df_inflacionPeriodo
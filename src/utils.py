import pandas as pd
import requests
import sqlite3
import os
import re
import logging
from datetime import datetime


def ingestion(configs) -> pd.DataFrame:
    """
    Função de ingestão dos dados.

    Consome dados da API https://randomuser.me/api/
    trazendo pelo menos 10 registros.

    Args:
        configs: Objeto de configuração

    Returns:
        pd.DataFrame: DataFrame com dados brutos
    """

    logging.info("🔄 Iniciando ingestão de dados da API")

    url = "https://randomuser.me/api/?results=10"

    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Erro na API: {response.status_code}")
        raise Exception(f"Erro na API: {response.status_code}")

    data = response.json()["results"]

    df = pd.json_normalize(data)

    logging.info(f"✅ Dados ingeridos com sucesso: {len(df)} registros")

    # salvar raw
    raw_path = "assets/raw.csv"
    os.makedirs("assets", exist_ok=True)
    df.to_csv(raw_path, index=False)

    logging.info(f"💾 Arquivo raw salvo em: {raw_path}")

    return df


def validation_inputs(df: pd.DataFrame, configs) -> bool:
    """
    Validação dos dados antes de persistência.

    Args:
        df (pd.DataFrame): Dados
        configs: Configuração

    Returns:
        bool
    """

    logging.info("🔍 Iniciando validação dos dados")

    log_path = "assets/log.txt"
    required_columns = ["name_first", "email"]

    os.makedirs("assets", exist_ok=True)

    with open(log_path, "a") as log:

        if df.empty:
            msg = "ERRO: DataFrame vazio"
            logging.error(msg)
            log.write(f"{datetime.now()} - {msg}\n")
            raise ValueError(msg)

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            msg = f"ERRO: Colunas ausentes: {missing}"
            logging.error(msg)
            log.write(f"{datetime.now()} - {msg}\n")
            raise ValueError(msg)

        msg = "Dados corretos"
        logging.info(f"✅ {msg}")
        log.write(f"{datetime.now()} - {msg}\n")

    return True


def preparation(df: pd.DataFrame, configs) -> bool:
    """
    Preparação dos dados.

    Etapas:
        - Renomeia colunas
        - Remove caracteres especiais
        - Ajusta tipos
        - Valida dados
        - Salva em SQLite

    Args:
        df (pd.DataFrame): Dados brutos
        configs: Configuração

    Returns:
        bool
    """

    logging.info("🛠️ Iniciando preparação dos dados")

    # renomear colunas
    logging.info("🔤 Renomeando colunas")
    df.columns = [col.lower().replace(".", "_") for col in df.columns]

    # remover caracteres especiais
    logging.info("🧹 Removendo caracteres especiais")
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(
            lambda x: re.sub(r"[^a-zA-Z0-9 ]", "", str(x))
        )

    # ajuste de tipos
    logging.info("🔢 Ajustando tipos de dados")
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    # validação
    validation_inputs(df, configs)

    # salvar SQLite
    logging.info("💾 Salvando dados no SQLite")

    db_path = "assets/database.db"
    conn = sqlite3.connect(db_path)

    df.to_sql("random_users", conn, if_exists="replace", index=False)
    conn.close()

    logging.info(f"✅ Dados salvos com sucesso em: {db_path}")

    return True
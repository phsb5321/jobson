# app/config.py
"""This module holds application-wide configurations."""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration settings."""

    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://serpapi.com/search.json"
    MONGO_URI = os.getenv("MONGO_URI")

    JOB_QUERIES = [
        "Engenheiro de Software",
        "Cientista de Dados",
        "Gerente de Projetos",
        "Engenheiro DevOps",
        "Desenvolvedor Frontend",
        "Desenvolvedor Backend",
        "Desenvolvedor Full Stack",
        "Desenvolvedor Mobile",
        "Analista de Dados",
        "Analista de Sistemas",
        "Administrador de Redes",
        "Administrador de Banco de Dados",
        "Especialista em Suporte de TI",
        "Analista de Segurança",
        "Engenheiro de Nuvem",
    ]

    BRAZILIAN_STATES = [
        "Acre",
        "Alagoas",
        "Amapá",
        "Amazonas",
        "Bahia",
        "Ceará",
        "Distrito Federal",
        "Espírito Santo",
        "Goiás",
        "Maranhão",
        "Mato Grosso",
        "Mato Grosso do Sul",
        "Minas Gerais",
        "Pará",
        "Paraíba",
        "Paraná",
        "Pernambuco",
        "Piauí",
        "Rio de Janeiro",
        "Rio Grande do Norte",
        "Rio Grande do Sul",
        "Rondônia",
        "Roraima",
        "Santa Catarina",
        "São Paulo",
        "Sergipe",
        "Tocantins",
    ]

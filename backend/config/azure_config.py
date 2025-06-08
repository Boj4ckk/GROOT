# config/azure_config.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(dotenv_path="backend/.env")
# Configuration pour Azure SQL Database
class AzureConfig:
    

    # Variables d'environnement pour Azure
    AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER")
    AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
    AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
    AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")
    
    # Connection string pour Azure SQL
    @property
    def database_url(self):
        return f"mssql+pyodbc://{self.AZURE_SQL_USERNAME}:{self.AZURE_SQL_PASSWORD}@{self.AZURE_SQL_SERVER}:1433/{self.AZURE_SQL_DATABASE}?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=no"


config = AzureConfig()
engine = create_engine(config.database_url, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
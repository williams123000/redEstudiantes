from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
# Cargar variables del archivo .env
load_dotenv()

def create_neo4j_connection():
    uri = os.getenv("NEO4J_URI")  # URI 
    username = os.getenv("NEO4J_USERNAME")  # Usuario 
    password = os.getenv("NEO4J_PASSWORD")  # Contraseña 
    
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver
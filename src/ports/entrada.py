import json
import os

# Caminho correto para o appsettings.json na pasta src
appsettings_path = os.path.join(os.path.dirname(__file__), "../appsettings.json")
with open(appsettings_path, "r", encoding="utf-8") as f:
    settings = json.load(f)

lista_individuos_path = settings.get("individualsListPath")
mock_data_path = settings.get("personaListPath")

#Mocka a entrada do terminal para obter o idPersona e a lista de indivíduos
#Para teste
def ler_entrada_terminal():
    id_persona = input("Digite o idPersona: ")

    with open(lista_individuos_path, "r", encoding="utf-8") as f:
        lista_individuos = json.load(f)

    with open(mock_data_path, "r", encoding="utf-8") as f:
        mock_data = json.load(f)

    id_persona_existe = any(persona.get("idPersona") == id_persona for persona in mock_data)
    
    if not id_persona_existe:
        print(f"idPersona '{id_persona}' não encontrado em personaList-trainee.json.")
        return None, None
    return id_persona, lista_individuos
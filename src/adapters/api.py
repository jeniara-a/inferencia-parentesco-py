import json
import os

#Mocka a entrada do terminal para obter o idPersona e a lista de indivíduos
#Para teste
def consultar_api(id_persona):
    appsettings_path = os.path.join(os.path.dirname(__file__), "../appsettings.json")
    
    with open(appsettings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)
        personaList = settings.get("personaListPath") 

    try:
        with open(personaList, "r", encoding="utf-8") as f:
            personas = json.load(f)

        # Busca o dicionário da persona pelo id
        for persona in personas:
            if persona.get("idPersona") == id_persona:
                return persona
    except FileNotFoundError:
        print("Arquivo de mock não encontrado.")
        return None 
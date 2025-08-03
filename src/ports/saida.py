import json
import csv
import os
import getpass
from datetime import datetime

appsettings_path = os.path.join(os.path.dirname(__file__), "../appsettings.json")
with open(appsettings_path, "r", encoding="utf-8") as f:
    settings = json.load(f)

usuario = getpass.getuser()
data_hora_str = datetime.now().strftime("%Y%m%d_%H%M%S")
caminho_saida_json = settings["saidaJsonPath"]
caminho_saida_csv = f"{settings['saidaCsvPath']}/{data_hora_str}-{usuario}.csv"

def salvar_saida_json(resultado, caminho=caminho_saida_json):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

def salvar_saida_csv(resultado, caminho=caminho_saida_csv):
    # Garante que o diretório existe
    dir_saida = os.path.dirname(caminho)
    if dir_saida:
        os.makedirs(dir_saida, exist_ok=True)

    with open(caminho, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["idPersona", "idIndividuo", "nomeIndividuo", "docIndividuo", "grauParentesco", "acuracia", "rateio"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for individuo in resultado.get("relacaoIndividuos", []):
            writer.writerow({
                "idPersona": resultado.get("idPersona", ""),
                "idIndividuo": individuo.get("idIndividuo", ""),
                "nomeIndividuo": individuo.get("nomeIndividuo", ""),
                "docIndividuo": individuo.get("docIndividuo", ""),
                "grauParentesco": individuo.get("grauParentesco", ""),
                "acuracia": individuo.get("acuracia", ""),
                "rateio": individuo.get("rateio", ""),
            })
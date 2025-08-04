import json
import csv
import os
import webbrowser
from datetime import datetime

appsettings_path = os.path.join(os.path.dirname(__file__), "../appsettings.json")
with open(appsettings_path, "r", encoding="utf-8") as f:
    settings = json.load(f)

usuario = "tester_robot"  # Substitua pelo seu nome de usuário ou obtenha dinamicamente se necessário
data_hora_str = datetime.now().strftime("%Y%m%d_%H%M%S")
caminho_saida_json = settings["saidaJsonPath"]
caminho_saida_csv = settings['saidaCsvPath']
caminho_saida_html = settings['saidaHtmlPath']

def abrir_html(caminho_arquivo=caminho_saida_html):
    caminho_absoluto = os.path.abspath(caminho_arquivo)
    webbrowser.open(f"file://{caminho_absoluto}")

def salvar_saida_json(resultado, caminho=caminho_saida_json):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

def salvar_saida_csv(resultado, caminho=caminho_saida_csv):
    # Garante que o diretório existe
    dir_saida = os.path.dirname(caminho)
    if dir_saida:
        os.makedirs(dir_saida, exist_ok=True)

    arquivo_existe = os.path.isfile(caminho)

    with open(caminho, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["idPersona", "idIndividuo", "nomeIndividuo", "docIndividuo", "grauParentesco", "acuracia", "rateio", "userName", "dataHora"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not arquivo_existe:
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
                "userName": usuario,
                "dataHora": data_hora_str,
            })

def gerar_relatorio_html(resultado, caminho_arquivo=caminho_saida_html):
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #dddddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr.acuracia-1 { background-color: #d4edda; } /* verde claro */
            tr.acuracia-0 { background-color: #f8d7da; } /* vermelho claro */
        </style>
        <title>Relatório de Inferência de Parentesco</title>
    </head>
    <body>
        <h2>Relatório de Inferência - ID Persona: {idPersona}</h2>
        <table>
            <thead>
                <tr>
                    <th>ID Indivíduo</th>
                    <th>Nome</th>
                    <th>Grau Parentesco Previsto</th>
                    <th>Acurácia</th>
                </tr>
            </thead>
            <tbody>
    """.format(idPersona=resultado["idPersona"])

    for relacao in resultado["relacaoIndividuos"]:
        classe = "acuracia-1" if relacao["acuracia"] == 1.0 else "acuracia-0"
        html += f"""
            <tr class="{classe}">
                <td>{relacao['idIndividuo']}</td>
                <td>{relacao['nomeIndividuo']}</td>
                <td>{relacao['grauParentesco']}</td>
                <td>{relacao['acuracia']}</td>
            </tr>
        """

    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(html)

    abrir_html(caminho_arquivo)
    print(f"Relatório HTML gerado em {caminho_arquivo}")

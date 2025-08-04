from domain.modelo_similaridade import ModeloSimilaridade
from domain.rateio import ratear_individuos
from rapidfuzz import fuzz
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from datetime import datetime
import numpy as np
import pandas as pd
import unicodedata
import re
import joblib
import json
import os
import webbrowser

class ServicoInferencia:

    MAPEAMENTO_GRAUS = {
        "filho": {"filho", "filha", "criança", "menino", "menina"},
        "conjuge": {"cônjuge", "conjugue", "esposo", "esposa", "marido", "mulher", "companheiro", "companheira"},
    }

    appsettings_path = os.path.join(os.path.dirname(__file__), "../appsettings.json")
    with open(appsettings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    caminhoModelo = settings["modeloPath"]
    caminho_saida_html = settings['saidaHtmlPath']

    def __init__(self):
        self.modelo = ModeloSimilaridade()
        try:
            self.modelo.carregar(self.caminhoModelo)
        except Exception:
            self.modelo.treinado = False
    
    @classmethod
    def gerar_relatorio_html(cls, resultado, caminho_arquivo=caminho_saida_html):
        nome_persona = resultado.get("nomePersona", "Desconhecido")
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        html = """
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #dddddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr.acuracia-1 {{ background-color: #d4edda; }}
                tr.acuracia-0 {{ background-color: #f8d7da; }}
                footer {{ margin-top: 40px; font-size: 12px; color: #888; }}
            </style>
            <title>Resultado Grau de Parentesco</title>
        </head>
        <body>
            <h2>Resultado Grau de Parentesco - Persona: {nome_persona}</h2>
            <table>
                <thead>
                    <tr>
                        <th>ID Indivíduo</th>
                        <th>Nome</th>
                        <th>Grau Parentesco Previsto</th>
                        <th>Acurácia</th>
                        <th>Rateio</th>
                        <th>Estado de Vida</th>
                    </tr>
                </thead>
                <tbody>
        """.format(nome_persona=nome_persona)

        for relacao in resultado["relacaoIndividuos"]:
            classe = "acuracia-1" if relacao["acuracia"] == 1.0 else "acuracia-0"
            estado_vida_str = "Vivo" if relacao.get("estadoVida", False) else "Falecido"
            html += f"""
                <tr class="{classe}">
                    <td>{relacao['idIndividuo']}</td>
                    <td>{relacao['nomeIndividuo']}</td>
                    <td>{relacao['grauParentesco']}</td>
                    <td>{relacao['acuracia']:.2f}</td>
                    <td>{relacao['rateio']:.2f}%</td>
                    <td>{estado_vida_str}</td>
                </tr>
            """

        html += f"""
                </tbody>
            </table>
            <footer>
                Relatório gerado em: {data_atual}
            </footer>
        </body>
        </html>
        """

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Relatório HTML gerado em: {caminho_arquivo}")

    @staticmethod
    def abrir_html(caminho_arquivo=caminho_saida_html):
        caminho_absoluto = os.path.abspath(caminho_arquivo)
        webbrowser.open(f"file://{caminho_absoluto}")

    @classmethod
    def normalizar_grau_indicado(cls, indicacao_raw):
        if not indicacao_raw:
            return "nenhum"
        indicacao = indicacao_raw.strip().lower()
        for grau_padrao, sinonimos in cls.MAPEAMENTO_GRAUS.items():
            if indicacao in sinonimos:
                return grau_padrao
        return "nenhum"

    @staticmethod
    def combinar_predicoes(prob1, prob2, classes=["conjuge", "filho", "nenhum"]):
        prob1 = np.array(prob1)
        prob2 = np.array(prob2)
        prob_final = (prob1 + prob2) / 2
        return classes[np.argmax(prob_final)], prob_final
    
    @staticmethod
    def normalizar_nome(nome):
        nome = nome.lower()
        nome = unicodedata.normalize('NFD', nome)
        nome = nome.encode('ascii', 'ignore').decode('utf-8')
        nome = re.sub(r'[^\w\s]', '', nome)
        stopwords = {'da', 'de', 'do', 'das', 'dos', 'e'}
        palavras = [p for p in nome.split() if p not in stopwords]
        nome = ' '.join(palavras)
        return nome.strip()

    def encontrar_grau_real(self, individuo, filhos, conjuge, limiar=70):
        nome_ind = self.normalizar_nome(individuo["nome"])
        indicacao = self.normalizar_grau_indicado(individuo.get("indicacao", ""))

        print(f"\n🔍 Analisando indivíduo: {individuo['nome']} (indicação: {indicacao})")
        print("Filhos vivos:")
        for f in filhos:
            print("  -", f["nome"])

        # Ajusta limiar se há indicação de filho
        limiar_filho = limiar - 10 if indicacao == "filho" else limiar
        for filho in filhos:
            nome_filho = self.normalizar_nome(filho["nome"])
            sim_filho = fuzz.token_sort_ratio(nome_ind, nome_filho)
            print(f"🔸 Similaridade com filho '{filho['nome']}': {sim_filho} (limiar: {limiar_filho})")
            if sim_filho >= limiar_filho:
                print("🔹 Grau de parentesco encontrado: filho")
                return "filho"

        # Ajusta limiar se há indicação de cônjuge
        limiar_conjuge = limiar - 10 if indicacao == "conjuge" else limiar
        if conjuge and conjuge.get("nome"):
            nome_conj = self.normalizar_nome(conjuge["nome"])
            sim_conj = fuzz.token_sort_ratio(nome_ind, nome_conj)
            print(f"🔸 Similaridade com cônjuge '{conjuge['nome']}': {sim_conj} (limiar: {limiar_conjuge})")
            if sim_conj >= limiar_conjuge:
                print("🔹 Grau de parentesco encontrado: cônjuge")
                return "conjuge"
            
        print("🔹 Grau de parentesco encontrado: nenhum")
        return "nenhum"
    
    def treinamento(self):
        # Treinamento
        # 1. Carregar do dataset
        caminhoDataSet= os.path.join(os.path.dirname(__file__), "../data/dataset_parentesco_simulado.csv")
        df = pd.read_csv(caminhoDataSet)

        # 2. Separar features e rótulo
        X = df[["sim_com_persona", "sim_com_filho", "sim_com_conjuge"]]
        y = df["grau_real"]

        # 3. Treinar modelo - Dividir em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.3, random_state=42)
        
        if not self.modelo.treinado or self.force_retrain:
            y = []
        for individuo in self.lista_individuos:
            grau_real = self.encontrar_grau_real(individuo, self.filhos, self.conjuge)
            y.append(grau_real)

        print("Rótulos de treino gerados por similaridade:", y)
        print("Total:", len(y), "Classes:", set(y))

        self.modelo.treinar(X, y)
        self.modelo.salvar(self.caminhoModelo)

        # 4 . Criar e treinar o modelo
        modelo = RandomForestClassifier(random_state=42)
        modelo.fit(X_train, y_train)

        # 4. Avaliar - Fazer previsões e calcular acurácia
        y_pred = modelo.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Acurácia do modelo: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))

    def inferir_relacoes(self, dados, force_retrain=False):
        
        # --- Preparação de dados ---
        persona = dados["dadosPersona"]
        dados_persona = persona.get("dadosPersona", {})
        lista_individuos = [i for i in dados["listaIndividuos"] if i.get("estadoVida", False) is True]
        filhos = dados_persona.get("filhos", {}).get("listaFilhos", [])
        filhos_vivos = [f for f in filhos if f.get("estadoVida", False) is True]
        conjuge = dados_persona.get("estadoCivil", {}).get("conjuge", {})
        conjuge_vivo = conjuge if conjuge.get("estadoVida", False) is True else None
        nome_conjuge_persona = conjuge_vivo.get("nome", "").strip() if conjuge_vivo else ""

        # --- Verifica se algum indivíduo é semelhante ao cônjuge ---
        conjuge_encontrado = any(
            fuzz.token_sort_ratio(ind["nome"].strip(), nome_conjuge_persona) >= 90
            for ind in lista_individuos
        )

        # --- Adiciona cônjuge desconhecido ---
        if nome_conjuge_persona and not conjuge_encontrado:
            lista_individuos.append({
                "idIndividuo": "desconhecido",
                "nome": nome_conjuge_persona,
                "docIndividuo": "n/a",
                "grauParentesco": "conjuge",
                "estadoVida": True
            })

        self.force_retrain = force_retrain
        self.lista_individuos = lista_individuos
        self.filhos = filhos_vivos
        self.conjuge = conjuge_vivo

        # --- Treinamento do modelo, se necessário ---
        if not self.modelo.treinado or force_retrain:
            X = []
            y = []
            for individuo in lista_individuos:
                X.append(self.modelo.extrair_features_1(individuo, persona, filhos_vivos, conjuge))
                X.append(self.modelo.extrair_features_2(individuo, persona, filhos_vivos, conjuge))
                grau_real = self.encontrar_grau_real(individuo, filhos_vivos, conjuge)
                y.append(grau_real)

            print("Rótulos de treino gerados por similaridade:", y)
            print("Total:", len(y), "Classes:", set(y))

            self.modelo.treinar(X, y)
            self.modelo.salvar(caminho=self.caminhoModelo)

        # --- Inferência ---
        X_inf_1 = [
            self.modelo.extrair_features_1(ind, persona, filhos_vivos, conjuge)
            for ind in lista_individuos
        ]

        predicoes1 = self.modelo.prever(X_inf_1)
        probs1 = self.modelo.model.predict_proba(X_inf_1)

        print("Predições 1 + probabilidades:", list(zip(predicoes1, probs1)))

        X_inf_2 = [
            self.modelo.extrair_features_2(ind, persona, filhos_vivos, conjuge)
            for ind in lista_individuos
        ]

        predicoes2 = self.modelo.prever(X_inf_2)
        probs2 = self.modelo.model.predict_proba(X_inf_2)

        print("Predições 2 + probabilidades:", list(zip(predicoes2, probs2)))

        # --- Combinar predições ---
        predicoes = []
        for p1, p2 in zip(probs1, probs2):
            classe_final, _ = self.combinar_predicoes(p1, p2)
            predicoes.append(classe_final)

        # --- Resultado final ---
        resultado = {
            "idPersona": dados["idPersona"],
            "relacaoIndividuos": []
        }

        for individuo, pred in zip(lista_individuos, predicoes):
            grau_real = self.encontrar_grau_real(individuo, filhos_vivos, conjuge)
            print(f"Comparando predição '{pred}' com grau_real '{grau_real}' para '{individuo['nome']}'")

            acuracia = 1.0 if pred == grau_real else 0.0

            resultado = {
                "idPersona": dados["idPersona"],
                "nomePersona": dados["dadosPersona"]["dadosPersona"].get("persona", "Desconhecido"),
                "relacaoIndividuos": []
            }

            resultado["relacaoIndividuos"].append({
                "idIndividuo": individuo["idIndividuo"],
                "nomeIndividuo": individuo["nome"],
                "docIndividuo": individuo.get("docIndividuo", ""),
                "grauParentesco": pred,
                "acuracia": acuracia,
                "rateio": 0.0,
                "estadoVida": individuo.get("estadoVida", True)
            })

        # --- Aplicar rateio ---
        ratear_individuos(resultado["relacaoIndividuos"], 100.0)

        self.gerar_relatorio_html(resultado)
        self.abrir_html()

        return resultado
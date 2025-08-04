from sklearn.ensemble import RandomForestClassifier
from rapidfuzz import fuzz
import pandas as pd
import joblib
import os

class ModeloSimilaridade:
    def __init__(self):
        self.model = RandomForestClassifier(class_weight="balanced")
        self.treinado = False

    def extrair_features_1(self, individuo, persona, filhos, conjuge):
        features = []
        # 1. Similaridade nome individuo com persona
        nome_individuo = individuo["nome"]
        persona_nome = persona["dadosPersona"]["persona"]
        similaridade = fuzz.token_sort_ratio(nome_individuo, persona_nome)
        features.append(similaridade)
        
        print(f"Similaridade entre '{nome_individuo}' e '{persona_nome}': {similaridade}")
        
        # 2. Similaridade nome com cada filho - pegar max ou média
        max_sim_filhos = 0
        for f in filhos:
            sim = fuzz.token_sort_ratio(individuo["nome"], f["nome"])
            if sim > max_sim_filhos:
                max_sim_filhos = sim
        features.append(max_sim_filhos)

        print(f"Máxima similaridade entre '{nome_individuo}' e filhos: {max_sim_filhos}")
        
        # 3. Similaridade nome com cada cônjuge - pegar max ou média
        max_sim_conjuge = 0
        if conjuge and conjuge.get("nome"):
            max_sim_conjuge = fuzz.token_sort_ratio(individuo["nome"], conjuge["nome"])
        features.append(max_sim_conjuge)

        return features

    def extrair_features_2(self, individuo, persona, filhos, conjuge):
        features = []
        # 4. Estado de vida (binário)
        persona_nome = persona["dadosPersona"]["persona"]
        features.append(1 if individuo.get("estadoVida") else 0)

        # 5. Possui nome do pai/mãe do individuo similar à persona
        nome_mae = individuo.get("nomeMae", "").lower()
        nome_pai = individuo.get("nomePai", "").lower()
        nome_persona = persona_nome.lower()
        sim_mae = fuzz.token_sort_ratio(nome_mae, nome_persona)
        sim_pai = fuzz.token_sort_ratio(nome_pai, nome_persona)
        sim_filiacao = max(sim_mae, sim_pai)
        features.append(sim_filiacao)

        # 6. Compartilhamento de sobrenome
        tokens_individuo = set(individuo["nome"].lower().split())
        tokens_persona = set(persona_nome.lower().split())
        sobrenomes_comuns = tokens_individuo.intersection(tokens_persona)
        features.append(1 if sobrenomes_comuns else 0)

        return features

    def treinar(self, X, y):
        self.model.fit(X, y)
        self.treinado = True

    def prever(self, X):
        return self.model.predict(X)

    def salvar(self, caminho):
        os.makedirs(os.path.dirname(caminho), exist_ok=True)  # Garante que o diretório existe
        joblib.dump(self.model, caminho)

    def carregar(self, caminho):
        self.model = joblib.load(caminho)
        self.treinado = True
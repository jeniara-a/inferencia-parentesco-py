import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from rapidfuzz import fuzz
import joblib
import os

class ModeloSimilaridade:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.treinado = False

    def extrair_features(self, individuo, persona, filhos, conjuge):
        features = [
            # Similaridade de nomes
            fuzz.token_sort_ratio(individuo["nome"], persona["persona"])
        ]
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

# # Biblioteca RapidFuzz: utilizada para calcular a similaridade entre strings de forma eficiente.
# # 1 - O método fuzz.token_sort_ratio é usado para calcular similaridade 
# # entre strings, ignorando a ordem das palavras.
# # 2 - Algoritmo RandomForestClassifier: utilizado para classificar relações de parentesco
# # com base em características extraídas dos dados.

# # Função de similaridade usando RapidFuzz
# def calcular_similaridade(nome1, nome2):
#     if not nome1 or not nome2:
#         return 0.0
#     return fuzz.token_sort_ratio(nome1, nome2) / 100

# # Dataset de exemplo
# df = pd.DataFrame([
#     {
#         "idPersona": "P001", "nomePersona": "João Silva",
#         "idIndividuo": "P002", "nomeIndividuo": "Carlos Silva",
#         "matchFilho": 1, "matchConjuge": 0, "label": "filho"
#     },
#     {
#         "idPersona": "P001", "nomePersona": "João Silva",
#         "idIndividuo": "P005", "nomeIndividuo": "Maria Oliveira",
#         "matchFilho": 0, "matchConjuge": 1, "label": "cônjuge"
#     },
#     {
#         "idPersona": "P001", "nomePersona": "João Silva",
#         "idIndividuo": "P010", "nomeIndividuo": "Joana Marques",
#         "matchFilho": 0, "matchConjuge": 0, "label": "nenhum"
#     },
# ])

# # Aplicar similaridade
# df["simNome"] = df.apply(
#     lambda row: calcular_similaridade(row["nomePersona"], row["nomeIndividuo"]),
#     axis=1
# )

# # Features e target
# X = df[["matchFilho", "matchConjuge", "simNome"]]
# y = df["label"]

# # Split e treino
# X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.4, random_state=42)
# clf = RandomForestClassifier(random_state=42)
# clf.fit(X_train, y_train)

# # Avaliação
# y_pred = clf.predict(X_test)
# print("\n✅ Relatório de Classificação:")
# print(classification_report(y_test, y_pred))

# # Inferência futura
# def inferir_relacao(matchFilho, matchConjuge, nomePersona, nomeIndividuo):
#     simNome = calcular_similaridade(nomePersona, nomeIndividuo)
#     entrada = pd.DataFrame([{
#         "matchFilho": matchFilho,
#         "matchConjuge": matchConjuge,
#         "simNome": simNome
#     }])
#     pred = clf.predict(entrada)[0]
#     prob = clf.predict_proba(entrada).max()
#     return {
#         "grauParentesco": pred,
#         "acuracia": round(float(prob), 2)
#     }

# # Exemplo de uso
# res = inferir_relacao(
#     matchFilho=1,
#     matchConjuge=0,
#     nomePersona="João Silva",
#     nomeIndividuo="Carlos da Silva"
# )
# print("\n📌 Resultado da inferência:", res)

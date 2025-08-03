from domain.modelo_similaridade import ModeloSimilaridade
import json
import os

class ServicoInferencia:

    appsettings_path = os.path.join(os.path.dirname(__file__), "../appsettings.json")
    with open(appsettings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    caminhoModelo = settings["modeloPath"]

    def __init__(self):
        self.modelo = ModeloSimilaridade()
        try:
            self.modelo.carregar(self.caminhoModelo)
        except Exception:
            self.modelo.treinado = False

    def inferir_relacoes(self, dados):
        persona = dados["dadosPersona"]
        filhos = persona.get("filhos", {}).get("listaFilhos", [])
        conjuge = persona.get("estadoCivil", {}).get("conjuge", {})
        lista_individuos = dados["listaIndividuos"]

        X = []
        for individuo in lista_individuos:
            X.append(self.modelo.extrair_features(individuo, persona, filhos, conjuge))

        if not self.modelo.treinado:
            y = []
            for individuo in lista_individuos:
                if individuo["idIndividuo"] in [f["idFilho"] for f in filhos]:
                    y.append("filho")
                elif conjuge and individuo["idIndividuo"] == conjuge.get("idConjuge"):
                    y.append("conjuge")
                else:
                    y.append("nenhum")
            self.modelo.treinar(X, y)
            self.modelo.salvar("data/modelo_rf.joblib")

        predicoes = self.modelo.prever(X)
        # Exemplo: acuracia 1.0 para predição igual ao esperado, 0.0 caso contrário (ajuste conforme seu critério)
        resultado = {
            "idPersona": dados["idPersona"],
            "relacaoIndividuos": []
        }
        for individuo, pred in zip(lista_individuos, predicoes):
            if individuo["idIndividuo"] in [f["idFilho"] for f in filhos]:
                acuracia = 1.0 if pred == "filho" else 0.0
            elif conjuge and individuo["idIndividuo"] == conjuge.get("idConjuge"):
                acuracia = 1.0 if pred == "conjuge" else 0.0
            else:
                acuracia = 0.0 if pred == "nenhum" else 0.0

            resultado["relacaoIndividuos"].append({
                "idIndividuo": individuo["idIndividuo"],
                "nomeIndividuo": individuo["nome"],
                "grauParentesco": pred,
                "acuracia": acuracia
            })
        return resultado

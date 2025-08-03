from typing import List

class Individuo:
    def __init__(self, id_individuo: str, nome: str):
        self.id_individuo = id_individuo
        self.nome = nome

class Persona:
    def __init__(self, id_persona: str, nome: str, filhos: List[Individuo], conjuge: Individuo = None):
        self.id_persona = id_persona
        self.nome = nome
        self.filhos = filhos
        self.conjuge = conjuge
# 🧠 🎯 PoC - Inferência de Parentesco para Sucessão de 1º Grau - baseado em Random Forest

Este projeto é uma Prova de Conceito (PoC) que utiliza um modelo de **Machine Learning supervisionado** para, dada uma `Persona` e uma lista de `indivíduos` relacionados (citados ou aleatórios), **inferir o grau de parentesco para sucessão de 1º grau (filhos e cônjuges vivos)** com base em **características extraídas por similaridade textual**.

---

## 📦 Estrutura do Dataset

O dataset é composto por amostras que contêm:

- A **persona** (nome da pessoa de referência);
- Um conjunto de **indivíduos** (potencialmente filhos, cônjuges ou sem parentesco com a persona);
- **Features extraídas automaticamente**, incluindo:
  - Similaridade do nome do indivíduo com o nome da persona;
  - Similaridade com os nomes dos filhos da persona;
  - Similaridade com o nome do cônjuge da persona.

Cada linha representa uma instância de inferência, com características numéricas (similaridades variando de 0 a 100) e um **rótulo categórico real**: `filho`, `conjuge` ou `nenhum`.

---

## 🧠 Modelo de Inferência

O modelo utilizado é o `RandomForestClassifier`, da biblioteca **Scikit-learn**, ideal para tarefas de **classificação** com dados tabulares. Ele oferece boa performance e permite interpretação da importância das features.

---

## 📊 Comparativo entre Modelos

| Modelo                         | Prós                                                                                                                                 | Contras                                                                                       |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| **Random Forest** ✅          | - Robusto a ruído<br>- Boa performance com dados tabulares<br>- Interpretação de importância das features ✅                         | - Lento em datasets grandes<br>- Pode não capturar relações complexas<br>- Fraco com texto ✅ |
| XGBoost / LightGBM / CatBoost | - Excelente acurácia<br>- Bom com dados desbalanceados<br>- CatBoost trata bem dados categóricos<br>- Rápido para inferência        | - Requer mais tuning<br>- Menos interpretável<br>- Sensível a outliers                       |
| Redes Neurais (MLP)           | - Suporta embeddings<br>- Capta relações não-lineares<br>- Escala bem para grandes volumes                                          | - Requer mais dados<br>- Menos interpretável<br>- Requer normalização e tuning               |
| Transformers (ex: BERT)       | - Excelente para texto<br>- Capta contexto e semântica<br>- Ideal para uso com OCR ou nomes longos                                  | - Alto custo computacional<br>- Requer muitos dados ou fine-tuning<br>- Inferência lenta     |
| KNN                           | - Simples de implementar<br>- Boa baseline com embeddings<br>- Intuitivo para tarefas de similaridade                              | - Não escala bem<br>- Sensível a ruído<br>- Difícil otimização de hiperparâmetros            |

---

## 📚 Classificação de Grau de Parentesco (conforme Código Civil)

### Ordem de Prioridade e Grupos de Herdeiros

1. **Descendentes**: Filhos, netos, bisnetos, etc. **(1º grau)**
2. **Ascendentes**: Pais, avós, bisavós, etc.
3. **Cônjuge/Companheiro**: Herda em conjunto com descendentes ou ascendentes, conforme regime de bens. **(1º grau)**
4. **Colaterais**: Irmãos, sobrinhos, tios, primos, etc.

> 📌 *Referência: agosto/2025*

---

## 💰 Rateio - Sucessão

| Grau de Parentesco | Peso no Rateio       |
|--------------------|----------------------|
| Cônjuge            | 0.5                  |
| Filho              | 0.5 / N filhos       |
| Nenhum             | 0                    |

---

## ✅ Regras e Requisitos de Inferência

- Apenas indivíduos com `"estadoVida": true` devem participar da inferência e do rateio.
- Se a `persona` for **casada(o)** e o **cônjuge não estiver listado** em `listaIndividuos`, o sistema deve:
  - Reservar **50% do valor para um cônjuge fictício (desconhecido)**;
  - Ratear os outros 50% entre os **filhos com acurácia >= 1.0**;
  - Incluir o **cônjuge desconhecido** no campo `relacaoIndividuos` do resultado da inferência.
- Se a `persona` tiver **filhos vivos** declarados e o **filho não estiver listado** em `listaIndividuos`, o sistema deve:
    - Reservar o valor correspondente do rateio para o filho vivo
    - Incluir o **filho desconhecido** no campo `relacaoIndividuos` do resultado da inferência.
---

## 📄 Resultado

O resultado será apresentado conforme abaixo, disponível no arquivo `output`, nos formatos **.csv**, **.html** e **.json**  
➡️ Exemplo com dataset fictício disponível em: [https://jeniara-a.github.io/inferencia-parentesco-py/](https://jeniara-a.github.io/inferencia-parentesco-py/)

---

### 🧍‍♀️ Persona:

| **idPersona**              | **nomePersona**          | **estadoCivil**                                | **numFilhosVivos**                    |
|----------------------------|--------------------------|------------------------------------------------|----------------------------------------|
| id identificador da persona (tabular) | nome da persona (tabular) | estado civil da persona (casado(a), solteiro(a), viúvo(a), etc.) | número de filhos vivos da persona (0, 1, 2, 3, …) |

---

### 👥 Relação de Indivíduos Classificados:

| **idIndividuo**           | **nomeIndividuo**         | **grauParentesco**                                                   | **grauResultado**                                                  | **estadoVida**                              | **rateio**                          |
|---------------------------|---------------------------|---------------------------------------------------------------------|-------------------------------------------------------------------|---------------------------------------------|-------------------------------------|
| id identificador do indivíduo (tabular) | nome do indivíduo (tabular) | grau de parentesco indicado pelo indivíduo (cônjuge, filho ou nenhum/outro) (tabular) | grau de parentesco inferido via modelo (cônjuge, filho ou nenhum/outro) | estado de vida do indivíduo (true = vivo, false = falecido) (tabular) | percentual de rateio inferido via modelo |

---

## 🚧 Status

📅 Projeto em construção — *última atualização: 05/08/2025*
 

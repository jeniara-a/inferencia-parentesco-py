
def ratear_individuos(individuos, valor_total):
    """
    Faz o rateio do valor_total entre indivíduos filtrando por acurácia >= 1.0,
    e aplicando pesos diferentes conforme o grau de parentesco:
    
    Regras:
    - Cônjuge: recebe 50% do valor_total
    - Filhos: dividem 50% do valor_total igualmente
    - Nenhum: recebe 0
    
    Args:
        individuos (list): lista de dicts com pelo menos as chaves:
            - 'grauParentesco' (str): 'cônjuge', 'filho' ou 'nenhum'
            - 'acuracia' (float)
        valor_total (float): valor total para rateio
    
    Returns:
        list: indivíduos que receberam valor_rateado na chave 'valor_rateado'
    """
    
    # Filtra indivíduos com acurácia >= 1.0
    filtrados = [i for i in individuos if i.get('acuracia', 0) >= 1.0]
    
    if not filtrados:
        return []

    # Separa cônjuge e filhos
    conjuge = [i for i in filtrados if i.get('grauParentesco') == 'cônjuge' or i.get('grauParentesco') == 'conjuge']
    filhos = [i for i in filtrados if i.get('grauParentesco') == 'filho' or i.get('grauParentesco') == 'filha']
    
    # Total para filhos (50%) dividido entre todos os filhos
    valor_conjuge = 0.5 * valor_total if conjuge else 0
    valor_filhos = valor_total - valor_conjuge

    # Distribui valor para cônjuge (se houver mais de um, divide igualmente)
    n_conjuge = len(conjuge)
    valor_conjuge_por_individuo = valor_conjuge / n_conjuge if n_conjuge > 0 else 0

    # Distribui valor para filhos
    n_filhos = len(filhos)
    valor_filho_por_individuo = valor_filhos / n_filhos if n_filhos > 0 else 0

    # Atualiza o campo rateio no resultado original (todos os indivíduos)
    for i in individuos:
        if i.get('acuracia', 0) < 1.0:
            i['rateio'] = 0
        elif i.get('grauParentesco') == 'cônjuge' or i.get('grauParentesco') == 'conjuge':
            i['rateio'] = round(valor_conjuge_por_individuo, 2)
        elif i.get('grauParentesco') == 'filho' or i.get('grauParentesco') == 'filha':
            i['rateio'] = round(valor_filho_por_individuo, 2)
        else:
            i['rateio'] = 0

    # Retorna só os filtrados (com acurácia >= 1.0 e valores já atribuídos)
    return filtrados

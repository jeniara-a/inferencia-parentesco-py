from ports.entrada import ler_entrada_terminal
from ports.saida import salvar_saida_csv, salvar_saida_json
from adapters.api import consultar_api
from domain.servico_inferencia import ServicoInferencia

def main():
    # 1. Entrada de Dados
    # Obtém através idPersona do personaList-trainee.json a relacao de dados da persona e os individuos que pleiteiam parentesco
    id_persona, lista_individuos = ler_entrada_terminal()

    if not id_persona or not lista_individuos:
        print("idPersona ou lista de indivíduos não encontrados. Encerrando execução.")
        return

    # 2. Consulta API externa para obter dados da persona
    dados_persona = consultar_api(id_persona)

    # 3. Consolida dados em um único dicionário
    dados_entrada = {
        "idPersona": id_persona,
        "dadosPersona": dados_persona,
        "listaIndividuos": lista_individuos
    }

    # 4. Realiza inferência de parentesco
    servico = ServicoInferencia()
    resultado = servico.inferir_relacoes(dados_entrada)

    # 5. Salva resultado em arquivo
    salvar_saida_json(resultado)
    salvar_saida_csv(resultado)
    print("Inferência concluída. Resultados salvos em output.json e output.csv.")

if __name__ == "__main__":
    main()



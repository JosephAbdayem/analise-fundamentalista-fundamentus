from fundamentus import analyze_stocks, get_data
import pandas as pd
import waiting_bar

def data_to_csv():
    """
    Coleta dados do Fundamentus e os grava em um arquivo CSV chamado 'dados.csv'.
    """
    data = get_data()
    formatted_data = {outer_key: {inner_key: float(inner_value) 
                                  for inner_key, inner_value in outer_value.items()}
                      for outer_key, outer_value in data.items()}

    df = pd.DataFrame.from_dict(formatted_data).transpose().rename(columns={'index': 'Ticker'})
    df.to_csv('dados.csv', sep=';', index=False)

def data_to_csv_filtrados():
    """
    Coleta e filtra dados do Fundamentus usando a função analyze_stocks,
    gravando os resultados em 'dados_filtrados.csv'.
    """
    data = analyze_stocks(get_data())
    formatted_data = {outer_key: {inner_key: float(inner_value) 
                                  for inner_key, inner_value in outer_value.items()}
                      for outer_key, outer_value in data.items()}

    df = pd.DataFrame.from_dict(formatted_data).transpose().rename(columns={'index': 'Ticker'})
    df.to_csv('dados_filtrados.csv', sep=';', index=False)

if __name__ == '__main__':
    overwrite_msg = input('Deseja criar um arquivo CSV com os dados mais atualizados do Fundamentus? Isso sobrescreverá os dados existentes. Pressione "Y" para sim: ')

    if overwrite_msg.upper() == 'Y':
        start_msg = waiting_bar.WaitingBar('Iniciando download de dados...')
        data_to_csv()
        data_to_csv_filtrados()
        start_msg.stop()
        print('Confira os dados no arquivo "funamentus.csv".')

    input('Pressione qualquer tecla para fechar.')

import requests
import json
import mysql.connector
from datetime import datetime

def buscarDados():
    # data_cotacao = datetime.today().strftime('%m-%d-%Y')
    date_cotacao = '05-09-2022'
    request = requests.get(f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{date_cotacao}'&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao")
    todo = json.loads(request.content)
    dados = todo['value']

    if len(dados)!=0:  
        return dados[0]['cotacaoVenda']
    else:
        return 'Nada'

if __name__ == '__main__':
    if buscarDados() != 'Nada':
        date = datetime.today().strftime('%Y-%m-%d')
        date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        print(date)
        print(date_time)
        conexao = mysql.connector.connect(
            host='localhost',
            database='database',
            user='root',
            password=''
        )
        try:
            cursor = conexao.cursor()
            cursor.execute(f"INSERT INTO valores (`data`, `dolar`, `ativo`, `excluido`, `usuario_id_atualizacao`, `data_atualizacao`, `ny`, `diferencial`, `datasqlserver`) VALUES ('{date}', {buscarDados()}, 1, 1, 12441, '{date_time}', 0.0000, 0.0000, '{date_time}')")
            conexao.commit()
            cursor.close()

            print("Usuário cadastrado com sucesso!")
        except:
            print("Ocorreu um erro na inserção do usuário")

    else:
        print('SEM COTAÇÃO')

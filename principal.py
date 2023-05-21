#   Importações
import sqlite3 as conector
import pandas
from modelo import Municipio, Covid

#   Variáveis de Operações
conn = None
cursor = None

#   Envolvemos nosso código em um bloco Try, para podermos tratarmos possíveis exceções.
try:
    #   Iniciando a conexão ao banco de dados e o cursor para execuções.
    conn = conector.connect('covidind.db')
    cursor = conn.cursor()

    #   Efetuando a iteração sobre o arquivo "covid_rj.csv"
    #   obtido na URL(https://sistemas.saude.rj.gov.br/tabnetbd/dhx.exe?covid19/esus_sivep.def).
    with open("dados/covid_rj.csv") as dados:
        dados.readline()
        for linha in dados:
            codigo, nome, casos_2020, casos_2021 = linha.strip().split(';')
            print(codigo, nome, casos_2020, casos_2021)

            municipio = Municipio(codigo, nome)

            comando_mun = '''INSERT INTO Municipio VALUES (:codigo, :nome)'''
            # cursor.execute(comando_mun, vars(municipio))

            comando_cov = '''INSERT INTO Covid VALUES (:codigo, :ano, :casos)'''
            cov_2020 = Covid(codigo, 2020, int(casos_2020))
            cov_2021 = Covid(codigo, 2021, int(casos_2021))
            # cursor.execute(comando_cov, vars(cov_2020))
            # cursor.execute(comando_cov, vars(cov_2021))

    #   Iniciamos a iteração ao arquivo (populacao.csv) obtido pelo IBGE
    #   Estimativa de Populacao para os anos de 2020 e 2021.
    #   URL(https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?edicao=17283&t=downloads)
    with open("dados/populacao.csv") as dados:
        dados.readline()
        for linha in dados:
            codigo, nome, pop_2020, pop_2021 = linha.strip().split(';')
            print(codigo, nome, pop_2020, pop_2021)

            comando_pop = '''INSERT INTO Populacao VALUES (:codigo, :ano, :populacao)'''
            # cursor.execute(comando_pop, {"codigo": codigo, "ano": 2020, "populacao": pop_2020})
            # cursor.execute(comando_pop, {"codigo": codigo, "ano": 2021, "populacao": pop_2021})

    #   Determinamos nossa query para recuperar os valores Nome da Tabela Municipio,
    #   Casos da Covid e População da Tabela Polulacão
    #   Utilizamos o SELECT JOIN para relacionar as tabelas pelo valor código de cada.
    #   Vale lembrar que o codigo das Tabelas Covid e Populacao são por chave estrangeira de Municipio.
    comando = '''SELECT Municipio.nome, Covid.casos, Populacao.populacao
                FROM Municipio 
                JOIN Covid ON Municipio.codigo = Covid.codigo 
                JOIN Populacao ON Municipio.codigo = Populacao.codigo
                WHERE Covid.ano=:ano AND Populacao.ano=:ano;'''

    #   Com a palavra reservada WHERE do SQL, definimos nossa regra para a execução, que será pelo ano.
    #   Logo, definimos nosso dicionário para suprir.
    ano = {"ano": 2021}
    cursor.execute(comando, ano)
    registros = cursor.fetchall()
    # print(registros[0])
    # print(f'{"municipio":30} - {"casos":5}- {"populacao":9} - {"incidencia"}')
    # for registro in registros:
    #     incidencia = registro[1] / registro[2]
    #     print(f'{registro[0]:30} - {registro[1]:5} - {registro[2]:9} - {incidencia:.6f}')

    resultado = pandas.read_sql(sql=comando, con=conn, params=ano)
    resultado['incidencia'] = 100 * resultado['casos'] / resultado['populacao']
    # print(resultado['incidencia'].describe())
    print(resultado.loc[resultado['incidencia'].idxmax()])

    conn.commit()

#   Definimos nossas Exceções.
except conector.OperationalError as errn:
    print("ERRO: Erro de Operação. ", errn)
except conector.DatabaseError as errn:
    print("ERRO: Erro de Banco de Dados. ", errn)
#   Definimos o nosso Finally para manter a robustes do código.
finally:
    if conn:
        cursor.close()
        conn.close()

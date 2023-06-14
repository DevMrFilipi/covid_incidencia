# *COVID-19 Incidência - Rio de Janeiro, Brasil #
{
    Projeto utilizando conhecimentos acadêmicos, na Linguagem de Programação Python e 
    Banco de Dados (SQLite).
    Utilizando as melhores práticas para manipulação de dados, este projeto tem como
    finalidade obter a incidência (quantidade dos casos / população do município) 
    da Doença em cada Município do Estado escolhido.
    
    Comentário > "Está é apenas o esqueleto do Software, pretendo implementar uma interface em breve."

    Etapas >

            1° Obter as informações necessárias, pelos arquivos que contenham as informações
               entre os anos de 2020 e 2021, da população de cada Município do Estado e os casos
               de covid com base no Ano de Notificação dos Casos confirmados.
               Os arquivos serão commitados junto com o projeto, mas, caso queira obter os originais,
               seguem os links 
               (Sistema de Saúde do Rio de Janeiro: https://sistemas.saude.rj.gov.br/tabnetbd/dhx.exe?covid19/esus_sivep.def)
               (IBGE Estimativa de População: https://www.ibge.gov.br/estatisticas/sociais/populacao/9103-estimativas-de-populacao.html?edicao=17283&t=downloads)
            
            2°  Modelaremos o nosso Banco de Dados com as Tabelas necessárias para o passo 3°. As informações
                serão datadas neste arquivo para fins de prevenção caso o arquivo "covidind.db" não seja commitado.
            
            3° Utilizaremos o nosso algoritmo em Python para inserir(povoar) as informações em nosso Banco de Dados, logo após
               trabalharemos na operação necessária para obtermos a incidência utilizando tanto os métodos de iteração dos registros
               como a utilização da Biblioteca pandas para conseguirmos mais informações
               
}  

_Queries em SQL utilizadas para modelagem do Banco de Dados SQLite utilizado no Projeto._

    ________________________________________________________
        
        CREATE TABLE Municipio (
            codigo INTEGER NOT NULL,
            nome VARCHAR(32) NOT NULL,
            PRIMARY KEY(codigo)
        );
        
        CREATE TABLE Covid (
            codigo INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            casos INTEGER NOT NULL,
            PRIMARY KEY (codigo, ano),
            FOREIGN KEY (codigo) REFERENCES Municipio(codigo)
        );

        CREATE TABLE Populacao (
            codigo INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            populacao INTEGER NOT NULL,
            PRIMARY KEY (codigo, ano),
            FOREIGN KEY (codigo) REFERENCES Municipio(codigo)
        );

    _________________________________________________________

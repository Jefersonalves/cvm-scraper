import glob
import psycopg2                                               
import pandas as pd
from psycopg2.extras import execute_values

class StoreACMData:
    """
    Classe que lida com a criação da conexão com o banco de dados,
    criação da tabela e inserção de dados dos arquivos no banco de dados postgres
    para os dados da ACM

    Examples
    --------
    >>> db_store = StoreACMData(user, password, host, port, database, table)
    >>> db_store.cria_tabela()
    >>> db_store.insere_arquivo("data/inf_diario_fi_202001.csv")
    >>> db_store.encerra_conexao()
    """
    def __init__(self, user, password, host, port, database, table):
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database
        self._table = table
        self.cria_conexao_postgres()

    def cria_conexao_postgres(self):
        """
        cria o objeto de conexão com o banco de dados postgres e o cursor do bd
        
        Self
        -------
        self.connection: objeto de conexão com o postgres
        self.cursor: cursor do banco de dados
        """
        self.connection = psycopg2.connect( 
            user = self._user, 
            password = self._password, 
            host = self._host, 
            port = self._port,
            database = self._database 
        )

        self.cursor = self.connection.cursor()

    def insere_lista_valores(self, value_list):
        """
        insere uma lista de objetos no banco de dados
        
        Parameters
        -----------
        value_list: list of tuple
            lista das tuplas com os valores dos registros a serem inseridos
        """
        for value in value_list: #insere elementos um a um, pode ser otimizado posteriormente
            query = "INSERT INTO {} (CNPJ_FUNDO, DT_COMPTC, VL_TOTAL, VL_QUOTA, VL_PATRIM_LIQ, CAPTC_DIA, RESG_DIA, NR_COTST) VALUES {} ON CONFLICT (CNPJ_FUNDO, DT_COMPTC) DO NOTHING".format(self._table, value)
            try:
                self.cursor.execute(query)
            except Exception as e:
                print(e)

    def insere_arquivo(self, filename):
        """
        insere os valores de um arquivo csv no banco de dados
        
        Parameters
        -----------
        filename: str
            nome do arquivo csv cujos dados vão ser inseridos

        Notes
        ------
        os dados são iseridos na tabela self._table
        """
        informe = pd.read_csv(filename, sep=";")
        informe_tuple_list = list(informe.itertuples(index=False, name=None))
        informe_columns = list(informe)

        self.verifica_colunas(informe_columns) #verifica se o arquivo possui as colunas esperadas
        try:
        
            self.insere_lista_valores(informe_tuple_list)
            self.connection.commit() #se a operação foi realizada sem erros ela é confirmada
        except Exception as e:
            print(e) #usar logging posteriormente
            self.connection.rollback()

    def insere_lista_arquivos(self, file_list):
        """
        insere uma lista de arquivos

        Parameters
        -----------
        file_list: list of str
            nome do arquivo csv cujos dados vão ser inseridos

        Notes:
        ------
        os elementos de file_list podem ser caminhos para arquivos locais ou urls de
        arquivos remotos
        """
        for file in file_list:
            print("inserindo dados do arquivo {}".format(file))
            self.insere_arquivo(file)

    def verifica_colunas(self, columns):
        """
        verifica se os nomes das colunas são como esperado
        
        Parameters
        -----------
        columns: list of str
            lista dos nomes das colunas

        Notes
        -----
        Lança uma exceção caso as colunas não estejam dentro esperado 
        """
        expected_columns = [
            'CNPJ_FUNDO',
            'DT_COMPTC',
            'VL_TOTAL',
            'VL_QUOTA',
            'VL_PATRIM_LIQ',
            'CAPTC_DIA',
            'RESG_DIA',
            'NR_COTST'
        ]

        error_message = "as columas do arquivo não correspondem com o esperado"
        assert len(columns) == len(expected_columns), error_message
        assert all([a == b for a, b in zip(columns, expected_columns)]), error_message

    def verifica_tipos(self):
        """
        verifica se os tipos de dados das colunas do arquivo são como esperado
        """
        pass

    def cria_tabela(self):
        """
        cria tabela no banco de dados caso não exista

        Notes
        -----
        Lança uma exceção caso não seja possível criar a tabela
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS {} (
                CNPJ_FUNDO VARCHAR(18) NOT NULL,
                DT_COMPTC DATE NOT NULL,
                VL_TOTAL numeric NOT NULL,
                VL_QUOTA numeric NOT NULL,
                VL_PATRIM_LIQ numeric NOT NULL,
                CAPTC_DIA numeric NOT NULL,
                RESG_DIA numeric NOT NULL,
                NR_COTST int NOT NULL,
                INSERT_TIME timestamp NOT NULL DEFAULT NOW(),
                PRIMARY KEY (CNPJ_FUNDO, DT_COMPTC)
            );
        """.format(self._table)

        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except Exception as e:
            print(e)
            self.connection.rollback()

    def encerra_conexao(self):
        """
        encerra conexão com o banco de dados
        """
        self.connection.close()
        self.cursor.close()

    def recupera_tudo(self):
        """
        recupera todos os registros da tabela

        Returns
        -------
        lista dos registros
        """
        self.cursor.execute("""SELECT * from {}""".format(self._table))
        rows = self.cursor.fetchall()
        return rows

    def insere_arquivos_do_diretorio(self, path):
        """
        insere todos os arquivos csv do diretório
        
        Parameters
        -----------
        path: str
            caminho do diretório que contém os arquivos
        """
        files = glob.glob("*.csv")
        for file in files:
            self.insere_arquivo(file)

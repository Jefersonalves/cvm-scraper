import os
from scraper import CVMDataScraper
from db_manager import StoreACMData

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
database = os.environ['POSTGRES_DB']

host = "postgres" #se estiver executando do host use "localhost"
port = "5432"
table = "cvminformes"

db_store = StoreACMData(user, password, host, port, database, table)
db_store.cria_tabela()
count = db_store.conta_registros()

scraper = CVMDataScraper()

if count > 0:
    print("inserindo informe diário no banco de dados")
    informe_diario = scraper.gera_url_informe_diario()
    db_store.insere_arquivo(informe_diario)
else:
    print("inserindo arquivos retroativos no banco de dados")
    #recuperação dos arquivos
    urls_informes_retroativos = scraper.gera_urls_informes_retroativos()
    #caso seja necessário salvar os arquivos localmente use: scraper.download_informes_retroativos()
    #caso contrário os arquivos serão lidos direto das urls para popular o banco

    db_store.insere_lista_arquivos(urls_informes_retroativos)

db_store.encerra_conexao()
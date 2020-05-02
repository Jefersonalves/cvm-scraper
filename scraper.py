import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

class CVMDataScraper:
    """
    Classe que lida com a obtenção dos arquivos de informes do CVM.
    O CVM disponibliza demonstrativos contendo informações dos fundos de investimento no
    portal de dados abertos <http://dados.cvm.gov.br/dataset/fi-doc-inf_diario>

    Examples
    --------
    >>> scraper = CVMDataScraper()
    >>> scraper.download_informe_diario() #download do informe do dia atual
    >>> scraper.download_informes_retroativos() #download dos informes retroativos
    >>> #lista das urls de 1 de janeiro de 2020 até 1 de abril de 2020
    >>> lista_urls_arquivos = scraper.genera_urls_no_intervalo(datetime(2020, 1, 1), datetime(2020, 4, 1))
    >>> scraper.download_lista_informes(lista_urls_arquivos) #download de informes no intervalo
    """
    def __init__(self):
        self.file_url_prefix = "http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_"

    def download_informe(self, file_url):
        """
        faz o download do arquivo csv de informe do CMV
        
        Parameters
        ----------
        file_url : string
            url do arquivo csv de informes disponibilizado pelo CMV
        
        Notes
        -------
        salva o arquivo csv localmente
        """
        csv_file = requests.get(file_url)
        file_name = file_url.split("/")[-1]

        with open(file_name, "wb") as file:
            file.write(csv_file.content)

    def gera_url_informe_diario(self):
        """
        obtém a url do arquivo csv do informe do dia atual
        
        Returns
        -------
        url do arquivo de informe do dia atual
        """
        today = datetime.today()
        month_formated = today.strftime("%Y%m")

        file_url = "{}{}.csv".format(self.file_url_prefix, month_formated)
        return file_url

    def download_informe_diario(self):
        """
        faz o download somente do arquivo csv de informes do dia
        
        Notes
        -------
        salva o arquivo csv localmente
        """
        file_url = self.gera_url_informe_diario()
        self.download_informe(file_url)

    def gera_datas_no_intervalo(self, start_date, end_date):
        """
        gera a lista de datas entre o start_date e end_date mês a mês
        
        Parameters
        ----------
        start_date : datetime
            a data de início da que se deseja obter os informes
        end_date : datetime
            a data fim da que se deseja obter os informes
        
        Returns
        -------
        splits: list of datetime
            lista das datas mês a mês no período entre start_date e end_date
        """
        splits = []
        while start_date <= end_date:
            splits.append(start_date)
            start_date = start_date + relativedelta(months=+1) #incremento mensal
        return splits

    def genera_urls_no_intervalo(self, start_date, end_date):
        """
        gera as urls dos arquivos de informes do CVM no intervalo entre start_date e end_date
        
        Parameters
        ----------
        start_date : datetime
            a data de início da que se deseja obter as urls dos informes
        end_date : datetime
            a data fim da que se deseja obter as urls dos informes
        
        Returns
        -------
        files_urls: list of str
            lista das urls dos arquivos
        """
        dates = self.gera_datas_no_intervalo(start_date, end_date)
        formated_dates = [data.strftime("%Y%m") for data in dates]

        files_urls = ["{}{}.csv".format(self.file_url_prefix, date) for date in formated_dates]
        return files_urls

    def download_lista_informes(self, files_urls):
        """
        faz o download dos arquivos na lista de urls

        Parameters
        ----------
        files_urls : list of string
            lista das urls dos arquivos
        
        Notes
        -------
        salva os arquivos csv localmente
        """
        for file in files_urls:
            self.download_informe(file)

    def gera_urls_informes_retroativos(self):
        """
        gera as urls dos arquivos de informes do CVM desde janeiro de 2017 até a data atual.
        Janeiro de 2017 é o primeiro mês no qual os arquivos csv passaram a ser disponibilizados dessa forma
        
        Returns
        -------
        files_urls: list of str
            lista das urls dos arquivos
        """
        start_date = datetime(2017, 1, 1) #janeiro 2017
        end_date = datetime.today()

        files_urls = self.genera_urls_no_intervalo(start_date, end_date)
        return files_urls

    def download_informes_retroativos(self):
        """
        faz o download dos arquivos de informes do CVM desde janeiro de 2017 até a data atual

        Notes
        -------
        salva os arquivos csv localmente
        """
        files_urls = self.gera_urls_informes_retroativos()
        self.download_lista_informes(files_urls)
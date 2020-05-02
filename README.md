># cmv-scraper

Módulo para obtenção dos arquivos de informes do CVM.
O CVM disponibliza demonstrativos contendo informações dos fundos de investimento no
portal de dados abertos <http://dados.cvm.gov.br/dataset/fi-doc-inf_diario>

>## configurção do ambiente

1. instale o [docker](https://docs.docker.com/engine/install/ubuntu/)

2. instale o [docker-compose](https://docs.docker.com/compose/install/)

3. substitua os valores das variáveis de ambiente no arquivo `docker-compose.yml`.

4. coloque o ambiente de pé com o comando: 
```
sudo docker-compose up
```

>## popular o banco com os dados retroativos

use o comando:
>```sh
>sudo docker exec python-cvm python update_db.py
>```

Na primeira execução, quando o bd não possuir registros,
será feito a população do banco com os informes do CVM
desde janeiro de 2017. Nas demais execuções será feita a
atualização da base com o informe diário.

Para outras possibilidades de uso e carregamento dos dados
consulte os módulos `scraper.py` e `update_db.py`

>## execução diária

adiconar o comando no crontab do host:
>```sh
>30 23 * * * docker exec python-cvm python update_db.py
>```

>## acesso ao bd
```
sudo docker exec -it postgres-cvm psql -U cvm -d informes
```
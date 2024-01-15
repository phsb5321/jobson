# jobson

'INTRODUÇÃO AO PROJETO'

Este espaço fornece a documentação detalhada para o código Python utilizado para realizar consultas de empregos usando a API do SerpApi. O código inclui funcionalidades para buscar informações de empregos com base em um título de trabalho e localização específicos, salvar os dados em formato JSON e CSV, além de exibir uma parte dos resultados, como é proposto.

-COMO FUNCIONA O PROCESSO DE EXTRAÇÃO DOS DADOS DO SERP API:

.Bibliotecas necessárias: json, panda e request. 

.O ccódigo resgata a chave da SERPAPI para conseguir fazer o uso do programa, a URL base para a consulta o diretório onde os dados serão salvos e o caminho para o arquivo CSV.

.O código manda um reuest para o SERPAPI fazer uma busca de dados de um emprego específico (Ex. "Software Engineer") e com uma localização específica (Ex. "San Francisco, CA")

.Caso algum dado seja encontrado ele é transformado em JSON e salvo na pasta 'CSV_FILE_PATH' e é mostrado uma frase de confirmação. Caso não, também será mostrado uma frase confirmando que nenhum dado foi salvo.


_______________________________________________________________________________________

'COMO USAR'

# Mini-Projeto TrilhaSonora

O TrilhaSonora é um projeto em que o usuário consegue analisar informações musicais dos integrantes da organização do Trilha, tais como a de listas os usuários, descobrir playlists, ver o quão próximo é o gosto musical de dois integrante, etc, consegue analisar informações de músicas ou álbuns que estão em um catálogo Json (como a duração, a avaliação, etc...) e consegue fazer uma mini simulação de apps de reprodução de música, como colocar faixas na fila, tocar músicas, (o que diminui a fila conforme vão sendo reproduzidas). Todas essas interações são feitas pelo terminal e com o sistema dando intruções para orientar o usuário no input.

## Modelagem

### Classe Catalogo

A classe existe por que conseguimos organizar melhor as funções e os dados nela, uma vez que ela faz parte da Programação Orientada a Objetos, e por isso disso, podemos reaproveitar ela e todo o seu conteúdo e seus métodos em arquivos diferentes, o que evita algumas repetições. No __init__, ela cria uma fila vazia de músicas a serem reproduzidas, o arquivo JSON é carregado e os índices de busca são construídos. Depois, todas as funções são escritas para que seja possivel realizar operações com elas.

## Estruturas de dados

Dicionários foram utilizados para que a interpretação e manipulação dos dados em Python fosse feito da melhor maneira. 

Os índices de nome foram usados para que fosse possível localizar os IDs pelo nome sem ter que percorrer toda a lista (obs: os nomes são buscados todos em minúsculo por causa do .lower(), que deixa a entrada toda em minúsculo, independente da maneira que seja escrita).

Os índices de gênero são para cada consulta não tenha que percorrer todos as 20 mil conteúdos novamente

Para as filas, o deque foi utilizado para que fosse permitido que conteúdos fossem adicionados no final e remover o primeiro conteúdo de maneira mais eficiente que nas listas, formando uma fila otimizada.

É mais fácil encontrar interseções em conjuntos em Python, pois existem comandos para tal (&), transformar o conteúdo das playlists de duas pesssoas em conjuntos fica mais fácil de achar a interseção.


## Tratamento dos dados

Para os ratings ausentes ou em string, foi usado o .get(), pois, caso não exista, não quebra o programa. Daí, se existir, é convertido em float independentemente, para que tudo seja realizado seguindo o mesmo padrão

Para gêneros aninhados, uma função foi criada para que eles fossem percorridos com uma pilha, fazendo checagens a cada elemento se ele é uma lista, e, cada gênero foi adicionado em uma lista que depois foi colocada em ordem alfabética

Para os formatos de datas, tudo foi deixado na maneira ano-mês-dia, e uma função para deixar tudo assim foi criada

Para números que tivessem vírgulas, apenas usei o método .replace(",", "") para tirar as vírgulas da string (ja que vinham nesse formato) e depois era convertido para int

Para durações nulas, uma checagem sempre acontecia se o valor era nulo ou não (com if duracao is not None), se fosse nulo, apenas era ignorado, somando apenas o que se fosse conhecido

## Como executar

precisa apenas de Python 3.10 ou superior e nada mais, apenas executar e aproveitar

### Menu interativo

python3 cli.py catalogo_final.json

obs: o menu permanece aberto até que o 0 seja digitado

### Modo batch

python3 main.py consultas.json respostas.json

para ler as consultas de consultas.json, utiliza o catálogo final e gera o arquivo respostas.json

### Conferir

python3 conferir.py

para comparar as primeiras respostas com gabarito_publico.json

### Verificação 

foi executada com as 10 mil consultas do modo batch e o resultado foi 20/20 acertos
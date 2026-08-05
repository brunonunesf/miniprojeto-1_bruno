"""A classe Catalogo. Leia o README.md antes de começar.

Esta é a peça central do projeto: carrega o JSON uma vez, constrói os
índices no __init__ e expõe os 16 métodos que o main.py e o cli.py usam.
"""
# pedi para uma LLM me orientar, e nao fazer por mim, ja que nao sei nem pra onde ir inicialmente
import json # biblioteca para trabalhar com json
from collections import deque # para removermos e adicionarmos de maneira mais eficiente os itens da fila

class Catalogo:
    def __init__(self, caminho_json: str):
        with open(caminho_json, mode='r', encoding='utf-8') as arquivo: #with fecha e abre o arquivo automaticamente
            self.dados = json.load(arquivo) #lê e transforma para python
        self.conteudos_por_id = {}
        for conteudo in self.dados["conteudos"]:
            identificador = conteudo["id"]
            self.conteudos_por_id[identificador] = conteudo # conteudo eh um dicionario inteiro que eh adicionada em um valor de uma chave de outro
        self.usuarios_por_id = {}
        for usuario in self.dados["usuarios"]:
            identificador = usuario["id"]
            self.usuarios_por_id[identificador] = usuario
        self.fila = deque()

catalogo = Catalogo("catalogo_dev.json") # por isso que eh caminho_json: str, pois ele recebe uma string
print(len(catalogo.usuarios_por_id))
print(catalogo.usuarios_por_id["u01"])


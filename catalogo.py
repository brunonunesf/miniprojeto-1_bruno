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
        self.ids_usuario_por_nome = {}
        for usuario in self.dados["usuarios"]:
            identificador = usuario["id"]
            self.usuarios_por_id[identificador] = usuario

            nome = usuario["nome"].lower()
            self.ids_usuario_por_nome[nome] = identificador
        self.fila = deque() # -> estrutura de dados mais otimizada de uma fila

        self.conteudos_por_genero = {}
        for conteudo in self.dados["conteudos"]:
            generos = self._achatar_generos(conteudo.get("generos", []))
            for genero in generos:
                if genero not in self.conteudos_por_genero:
                    self.conteudos_por_genero[genero] = []
                self.conteudos_por_genero[genero].append(conteudo["id"])


    def listar_usuarios(self) -> list[str]: # '->' = RETORNA ; ou seja, a funcao retorna uma lista de strings
        nomes = []
        for usuario in self.usuarios_por_id.values():
            nomes.append(usuario["nome"])
        return sorted(nomes)

    def buscar_usuario_por_nome(self, nome: str) -> str | None: # retorna uma string ou um None caso o nome nao exista
        nome_normalizado = nome.lower()
        return self.ids_usuario_por_nome.get(nome_normalizado) # .get() para nao dar erro se nao existir

    def playlist_de(self, usuario_id: str) -> list[str] | None: # -> diz a playlist do usuario com o ID digitado
        usuario = self.usuarios_por_id.get(usuario_id)
        if usuario is None:
            return None
        return list(usuario["playlist"])

    def conteudo_na_posicao(self, usuario_id: str, posicao: int) -> str | None: # -> a faixa que esta em tal posicao na playlist de um usuario digitado pelo ID dele
        playlist = self.playlist_de(usuario_id)
        if playlist is None:
            return None
        if 0 > posicao or posicao >= len(playlist): #por mais que python permita posicoes negativas, nao queremos para nao ficar confuso
            return None
        return playlist[posicao]

    def intersecao_playlists(self, usuario_ids: list[str]) -> list[str]: # -> diz os ID's das musicas ou albuns semelhantes entre duas playlists de duas pessoas
        if not usuario_ids:
            return []
        conjuntos = []
        for usuario_id in usuario_ids:
            playlist = self.playlist_de(usuario_id)
            if playlist is None:
                return []
            conjuntos.append(set(playlist)) #set tira duplicatas da lista
            itens_comuns = conjuntos[0]
            for conjunto in conjuntos[1:]: # pra percorrer os itens restantes da lista e ver udo o que tem de semelhante
                itens_comuns = itens_comuns & conjunto
            return sorted(itens_comuns)

    def rating_de(self, conteudo_id: str) -> float | None: # -> diz o rating de cada musica de acordo com o ID
        conteudo = self.conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        rating = conteudo.get("rating")
        if rating is None:
            return None
        return float(rating)
    
    def duracao_total_de(self, conteudo_id: str) -> int | None: # -> diz a duracao total da musica ou do album, com operacoes distintas dependendo do que for
        conteudo = self.conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        if conteudo["tipo"] == "musica":
            return conteudo["duracao_seg"]
        duracao_total = 0
        for faixa in conteudo["faixas"]:
            duracao = faixa["duracao_seg"]
            if duracao is not None:
                duracao_total += duracao
        return duracao_total

    def _achatar_generos(self, valor) -> list[str]: # coloca os tipos de genero que uma musica tem em uma lista so, ja que eles podem vir em formato de lista dentro de lista
        pendentes = [valor]
        generos = []
        while pendentes:
            atual = pendentes.pop()
            if isinstance(atual, str): #checa se a variavel eh do tipo depois da virgula
                generos.append(atual)
            if isinstance(atual, list):
                pendentes.extend(atual) # se for uma lista, cada elemento separadamente vai ser adicionado em pendentes por causa do extend
        return sorted(generos)

    def generos_de(self, conteudo_id: str) -> list[str] | None: # diz os generos da musica e da forma "achatada"
        conteudo = self.conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        generos = conteudo.get("generos", []) # -> o [] eh para caso o genero nao existir, ele retornar uma lista vazia
        return self._achatar_generos(generos)

    
    def conteudos_do_genero(self, genero: str) -> list[str]: # diz todas as faixas que pertencem a tal genero
        conteudos = self.conteudos_por_genero.get(genero, [])
        return sorted(conteudos)

    def plataformas_de(self, conteudo_id: str) -> list[str] | None: # -> diz as plataformas que a faixa esta disponivel
        conteudo = self.conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        plataformas = conteudo.get("plataformas", []) 
        return sorted(plataformas)

    def data_adicionado_de(self, conteudo_id: str) -> str | None: # -> diz a data da faixa, na maneira YYYY-MM-DD
        conteudo = self.conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        data = conteudo["data_adicionado"]
        if "/" not in data:
            return data
        dia, mes, ano = data.split("/")
        return f"{ano}-{mes}-{dia}"

    def execucoes_de(self, conteudo_id: str) -> int | None: # -> quantas vezes a faixa foi executada -> albuns aparecem None 
        conteudo = self.conteudos_por_id.get(conteudo_id)
        if conteudo is None:
            return None
        engajamento = conteudo.get("engajamento")
        if engajamento is None:
            return None
        execucoes = engajamento.get("execucoes")
        if execucoes is None:
            return None
        if isinstance(execucoes, str):
            execucoes = execucoes.replace(",", "") # -> substitui virgulas por espacos vazios caso o numero esteja na forma 102,091 por exemplo, ficando 102091
        return int(execucoes)

    def enfileirar(self, conteudo_id: str) -> bool: # -> adiciona na fila
        if conteudo_id not in self.conteudos_por_id:
            return False
        self.fila.append(conteudo_id)
        return True

    def proximo(self) -> str | None: # -> remove o primeiro item da fila -> ordem FIFO
        if not self.fila:
            return None
        return self.fila.popleft()

    def fila_atual(self) -> list[str]:
        return list(self.fila)






#testes -> executam so se eu rodar diretamente esse arquivo
if __name__ == "__main__":
    catalogo = Catalogo("catalogo_dev.json") # por isso que eh caminho_json: str, pois ele recebe uma string
    print(catalogo.execucoes_de("t000002"))
    print(catalogo.execucoes_de("t000009")) # album -> None
    print(catalogo.execucoes_de("t01"))

    print(catalogo.fila_atual())

    print(catalogo.enfileirar("t000002"))
    print(catalogo.enfileirar("t000009"))
    print(catalogo.enfileirar("t000002"))
    print(catalogo.enfileirar("id-inexistente")) # None

    print(catalogo.fila_atual())
    print(catalogo.proximo())
    print(catalogo.fila_atual())

    print(catalogo.proximo())
    print(catalogo.proximo())
    print(catalogo.proximo()) # None, pq nao tem mais nada pra tirar
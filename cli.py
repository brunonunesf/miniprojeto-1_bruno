"""Menu interativo no terminal.

Uso: python cli.py catalogo_final.json
"""
import sys # le o que foi escrito no terminal

from catalogo import Catalogo # pra usar os metodos ja implementados

def mostrar_menu() -> None: # -> so pra exibir informacoes
    print()
    print("TrilhaSonora")
    print("============")
    print("1. Listar todos os usuários")
    print("2. Ver playlist completa de um usuário")
    print("3. Conteúdo na posição N da playlist")
    print("4. Interseção de playlists")
    print("5. Dados de um conteúdo")
    print("6. Conteúdos de um gênero")
    print("7. Enfileirar conteúdo")
    print("8. Tocar próximo da fila")
    print("9. Ver fila atual")
    print("0. Sair")

def mostrar_conteudos(catalogo: Catalogo, conteudo_ids: list[str]) -> None:
    if not conteudo_ids:
        print("Nenhum conteúdo encontrado")
        return
    for conteudo_id in conteudo_ids:
        descricao = catalogo.descricao_de(conteudo_id)
        print(f"- {descricao}")

def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python3 cli.py catalogo_final.json")
        return
    caminho_catalogo = sys.argv[1]
    catalogo = Catalogo(caminho_catalogo)

    while True:
        mostrar_menu()
        opcao = input("> ").strip() # obs: strip remove espacos em branco do inicio e do fim da string, ja o split divide a string em varias partes de acordo com um delimitador
        if opcao == "0":
            print("Até logo!")
            break

        if opcao == "1":
            usuarios = catalogo.listar_usuarios()
            for nome in usuarios:
                print(f"- {nome}")

        elif opcao == "2":
            nome = input("Nome do usuário: ").strip()
            usuario_id = catalogo.buscar_usuario_por_nome(nome)
            if usuario_id is None:
                print("Usuário não encontrado")
            else:
                playlist = catalogo.playlist_de(usuario_id)
                mostrar_conteudos(catalogo, playlist) # playlist sera uma lista

        elif opcao == "3":
            nome = input("Nome do usuário: ").strip()
            usuario_id = catalogo.buscar_usuario_por_nome(nome)
            if usuario_id is None:
                print("Usuário não encontrado")
                continue
            playlist = catalogo.playlist_de(usuario_id)
            quantidade = len(playlist)
            print(f"Playlist de {nome} tem {quantidade} itens (posições 1 a {quantidade}).")
            entrada = input("Qual posição? > ").strip()
            try:
                posicao_humana = int(entrada)
            except ValueError:
                print("Digite uma posição numérica")
                continue
            conteudo_id = catalogo.conteudo_na_posicao(usuario_id, posicao_humana-1)
            if conteudo_id is None:
                print("Posição inválida")
            else:
                print(catalogo.descricao_de(conteudo_id))

        elif opcao =="4":
            entrada = input("Digite os nomes separados por vírgulas: ").strip()
            nomes = [nome.strip() for nome in entrada.split(",") if nome.strip()]
            usuario_ids = []
            usuario_invalido = False
            for nome in nomes:
                usuario_id = catalogo.buscar_usuario_por_nome(nome)
                if usuario_id is None:
                    print(f"Usuário não encontrado: {nome}")
                    usuario_invalido = True
                    break
                usuario_ids.append(usuario_id)
            if usuario_invalido:
                continue
            intersecao = catalogo.intersecao_playlists(usuario_ids)
            mostrar_conteudos(catalogo, intersecao)

        elif opcao == "5":
            conteudo_id = input("ID do conteúdo: ").strip()
            descricao = catalogo.descricao_de(conteudo_id)
            if descricao is None:
                print("Conteúdo não encontrado")
                continue
            rating = catalogo.rating_de(conteudo_id)
            plataformas = catalogo.plataformas_de(conteudo_id)
            duracao = catalogo.duracao_total_de(conteudo_id)
            generos = catalogo.generos_de(conteudo_id)
            data = catalogo.data_adicionado_de(conteudo_id)
            execucoes = catalogo.execucoes_de(conteudo_id)
            print(f"Conteúdo: {descricao}")
            print("Rating: ", end="")
            if rating is None:
                print("Não informado")
            else:
                print(rating)
            print(f"Duração: {duracao}")
            print(f"Gênero(s): {', '.join(generos)}")
            print(f"Plataformas: {', '.join(plataformas)}")
            print(f"Adicionado em: {data}")
            if execucoes is not None:
                print(f"Execuções: {execucoes:,}") #obs, isso foi uma sugestao da IA para que o numero 12500000 fique 12,500,00

        elif opcao == "6":
            genero = input("Digite um gênero: ").strip()
            if not genero:
                print("Digite um gênero...")
                continue
            conteudo_ids = catalogo.conteudos_do_genero(genero)
            mostrar_conteudos(catalogo, conteudo_ids)

        

        else:
            print("Opção inválida.")
        


if __name__ == "__main__":
    main()


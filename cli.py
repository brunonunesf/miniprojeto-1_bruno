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

        elif opcao == 4:
            

        
        else:
            print("Opção inválida.")
        


if __name__ == "__main__":
    main()


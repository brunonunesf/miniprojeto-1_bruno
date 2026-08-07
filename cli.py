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
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()


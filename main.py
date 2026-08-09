
import json # para transformar estruturas json em python
import sys # para ler argumentos do terminal

from catalogo import Catalogo

def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python3 main.py consultas.json respostas.json") # esse eh o comando correto que deve ser feito e será mostrado caso a pessoa nao o digite
        return
    caminho_consultas = sys.argv[1]
    caminho_respostas = sys.argv[2] # esses dois recebem os textos digitados no terminal

    catalogo = Catalogo("catalogo_final.json")

    with open(caminho_consultas, mode="r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo) # json.load() converte o json em dicionario python

    respostas = {}
    for consulta in dados["consultas"]:
        identificador = str(consulta["id"])
        tipo = consulta["tipo"]
        parametros = consulta["parametros"]
        metodo = getattr(catalogo, tipo)
        resposta = metodo(**parametros) # transforma dicionarios em argumentos nomeados...? -> pelo o que eu entendi, fica metodo(**{"conteudo_id": "t000007"}) = metodo(conteudo_id="t000007")
        respostas[identificador] = resposta
    with open(caminho_respostas, mode="w", encoding="utf-8") as arquivo:
        json.dump(respostas, arquivo, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
    
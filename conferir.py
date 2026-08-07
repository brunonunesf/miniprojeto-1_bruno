# para comparar se as primeiras respostas batem com gabarito_publico.json

import json
def respostas_iguais(esperada, obtida) -> bool:
    if isinstance(esperada, float) and isinstance(obtida, (int, float)):
        return abs(esperada - obtida) <= 1e-6
    return esperada == obtida
def main() -> None:
    with open("gabarito_publico.json", mode="r", encoding="utf-8") as arquivo:
        gabarito = json.load(arquivo) # so lembrando, o json.load() converte o json em dicionario python
    with open("respostas.json", mode="r", encoding="utf-8") as arquivo:
        respostas = json.load(arquivo)
    acertos = 0
    for identificador, esperada in gabarito.items():
        if identificador not in respostas:
            print(f"Consulta {identificador}: resposta ausente")
            continue
        obtida = respostas[identificador]
        if respostas_iguais(esperada, obtida):
            acertos += 1
        else:
            print(f"Consulta {identificador}: ")
            print(f"esperada={esperada!r}, obtida={obtida!r}") # o !r exibe claramente strings, listas e None, pra achar melhor as diferencas
    print(f"Acertos: {acertos}/{len(gabarito)}")

if __name__ == "__main__":
    main()
import random
import string
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt



# modelos de dadops:

@dataclass
class Pessoa:
    nome: str
    idade: int

    def __repr__(self):
        return f"{self.nome}({self.idade})"


#shell sort


#aqui está o metodo shell sort, ele recebe uma lista e começa a ordenar por meio do shell sort
#uma função key para definir o critério de ordenação e um parâmetro reverse para ordenar em ordem decrescente se necessário
#o algoritmo utiliza uma sequência de gaps pré-definida para melhorar a eficiência da ordenação
def shell_sort(lista, key=lambda x: x, reverse=False):
    n = len(lista)
    gaps = [701, 301, 132, 57, 23, 10, 4, 1] #aqui mede a "distancia" entre os elementos que vao ser comparados 
    gaps = [g for g in gaps if g < n]
    if not gaps:  
        gaps = [1]  # se a lista for muito pequena, usa gap 1

    for gap in gaps:
        for i in range(gap, n):
            temp = lista[i] # o elemento atual é armazenado em temp
            j = i
            while j >= gap and ( # aqui ocorre a comparação e troca dos elementos. Esse processo continua até que o elemento temp esteja na posição correta
                (not reverse and key(lista[j - gap]) > key(temp)) or
                (reverse and key(lista[j - gap]) < key(temp))
            ):
                lista[j] = lista[j - gap]
                j -= gap
            lista[j] = temp # o elemento temp é colocado na posição correta


#gerando dados aleatorios

def gerar_numeros(n):
    return [random.randint(0, n * 10) for _ in range(n)]

def gerar_strings(n, tamanho=8):
    letras = string.ascii_uppercase
    return ["".join(random.choice(letras) for _ in range(tamanho)) for _ in range(n)]

def gerar_pessoas(n):
    nomes_base = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda",
                  "Felipe", "Gabriel", "Helena", "Igor", "Julia"]
    return [
        Pessoa(
            nome=random.choice(nomes_base) + str(random.randint(1, 99)),
            idade=random.randint(10, 80)
        )
        for _ in range(n)
    ]


#medindo o tempo

def medir_tempo_execucao(dados, key=lambda x: x, reverse=False):
    copia = dados.copy()
    inicio = time.perf_counter()
    shell_sort(copia, key=key, reverse=reverse)
    fim = time.perf_counter()
    return (fim - inicio) * 1000


#gerando graficos

def gerar_graficos(tamanhos, resultados, titulo, nome_arquivo):
    plt.figure()
    plt.plot(tamanhos, resultados["crescente"], marker="o", label="Crescente")
    plt.plot(tamanhos, resultados["decrescente"], marker="s", linestyle="--",
             label="Decrescente")
    plt.title(titulo)
    plt.xlabel("Tamanho da entrada (número de elementos)")
    plt.ylabel("Tempo de execução (ms)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig(nome_arquivo, dpi=300)


# testes com diferentes elementos

def rodar_experimentos():
    tamanhos = [100, 1_000, 10_000, 100_000]

    resultados_numeros = {"crescente": [], "decrescente": []}
    resultados_strings = {"crescente": [], "decrescente": []}
    resultados_pessoas = {"crescente": [], "decrescente": []}

    print("\nTESTES COM NÚMEROS")
    for n in tamanhos:
        dados_base = gerar_numeros(n)
        t_c = medir_tempo_execucao(dados_base)
        t_d = medir_tempo_execucao(dados_base, reverse=True)
        resultados_numeros["crescente"].append(t_c)
        resultados_numeros["decrescente"].append(t_d)
        print(f"{n:>7} elementos -> crescente: {t_c:.2f} ms | decrescente: {t_d:.2f} ms")

    gerar_graficos(tamanhos, resultados_numeros, "Shell Sort - Números", "shellsort_numeros.png")

    print("\nTESTES COM STRINGS")
    for n in tamanhos:
        dados_base = gerar_strings(n)
        t_c = medir_tempo_execucao(dados_base)
        t_d = medir_tempo_execucao(dados_base, reverse=True)
        resultados_strings["crescente"].append(t_c)
        resultados_strings["decrescente"].append(t_d)
        print(f"{n:>7} -> crescente: {t_c:.2f} ms | decrescente: {t_d:.2f} ms")

    gerar_graficos(tamanhos, resultados_strings, "Shell Sort - Strings", "shellsort_strings.png")

    print("\nTESTES COM OBJETOS")
    for n in tamanhos:
        dados_base = gerar_pessoas(n)
        t_c = medir_tempo_execucao(dados_base, key=lambda p: p.idade)
        t_d = medir_tempo_execucao(dados_base, key=lambda p: p.idade, reverse=True)
        resultados_pessoas["crescente"].append(t_c)
        resultados_pessoas["decrescente"].append(t_d)
        print(f"{n:>7} -> crescente: {t_c:.2f} ms | decrescente: {t_d:.2f} ms")

    gerar_graficos(tamanhos, resultados_pessoas, "Shell Sort - Objetos (Pessoa.idade)", "shellsort_pessoas.png")

    print("\n✔ Gráficos gerados e exibidos com sucesso!")


# demonstração de cada tipo de elemento

def demonstracao():
    print("DEMONSTRAÇÃO DO SHELL SORT")
    print("1 - Números")
    print("2 - Strings")
    print("3 - Objetos")
    opc = input("Escolha: ")

    print("\n1 - Crescente")
    print("2 - Decrescente")
    reverse = input("Escolha: ") == "2"

    dados = gerar_numeros(10) if opc == "1" else gerar_strings(10) if opc == "2" else gerar_pessoas(10)
    key = (lambda p: p.idade) if opc == "3" else (lambda x: x)

    print("\nOriginal:", dados)
    shell_sort(dados, key=key, reverse=reverse)
    print("Ordenada:", dados)
    print("\n✔ Demonstração concluída!")


#menu

if __name__ == "__main__":
    while True:
        print("1 - Demonstração")
        print("2 - Experimentos completos + gráficos")
        print("0 - Sair")
        op = input("Escolha: ")

        if op == "1":
            demonstracao()
        elif op == "2":
            rodar_experimentos()
        elif op == "0":
            print("Encerrado!")
            break
        else:
            print("Inválido!")

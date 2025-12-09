import random
import string
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt


# 1. MODELOS DE DADOS

@dataclass
class Pessoa:
    nome: str
    idade: int

    def __repr__(self):
        return f"{self.nome}({self.idade})"


# 2. SHELL SORT

def shell_sort(lista, key=lambda x: x, reverse=False):
    n = len(lista)
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]
    gaps = [g for g in gaps if g < n]
    if not gaps:
        gaps = [1]

    for gap in gaps:
        for i in range(gap, n):
            temp = lista[i]
            j = i
            while j >= gap and (
                (not reverse and key(lista[j - gap]) > key(temp)) or
                (reverse and key(lista[j - gap]) < key(temp))
            ):
                lista[j] = lista[j - gap]
                j -= gap
            lista[j] = temp


# 3. GERAÇÃO DE DADOS

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


# 4. MEDIÇÃO DE TEMPO

def medir_tempo_execucao(dados, key=lambda x: x, reverse=False):
    copia = dados.copy()
    inicio = time.perf_counter()
    shell_sort(copia, key=key, reverse=reverse)
    fim = time.perf_counter()
    return (fim - inicio) * 1000

# 5. GRÁFICOS (MODIFICADO PARA COLAB)

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


# 6. EXPERIMENTOS AUTOMÁTICOS

def rodar_experimentos():
    tamanhos = [100, 1_000, 10_000, 100_000]

    resultados_numeros = {"crescente": [], "decrescente": []}
    resultados_strings = {"crescente": [], "decrescente": []}
    resultados_pessoas = {"crescente": [], "decrescente": []}

    print("\n=== TESTES COM NÚMEROS ===")
    for n in tamanhos:
        dados_base = gerar_numeros(n)
        t_c = medir_tempo_execucao(dados_base)
        t_d = medir_tempo_execucao(dados_base, reverse=True)
        resultados_numeros["crescente"].append(t_c)
        resultados_numeros["decrescente"].append(t_d)
        print(f"{n:>7} elementos -> crescente: {t_c:.2f} ms | decrescente: {t_d:.2f} ms")

    gerar_graficos(tamanhos, resultados_numeros, "Shell Sort - Números", "shellsort_numeros.png")

    print("\n=== TESTES COM STRINGS ===")
    for n in tamanhos:
        dados_base = gerar_strings(n)
        t_c = medir_tempo_execucao(dados_base)
        t_d = medir_tempo_execucao(dados_base, reverse=True)
        resultados_strings["crescente"].append(t_c)
        resultados_strings["decrescente"].append(t_d)
        print(f"{n:>7} -> crescente: {t_c:.2f} ms | decrescente: {t_d:.2f} ms")

    gerar_graficos(tamanhos, resultados_strings, "Shell Sort - Strings", "shellsort_strings.png")

    print("\n=== TESTES COM OBJETOS ===")
    for n in tamanhos:
        dados_base = gerar_pessoas(n)
        t_c = medir_tempo_execucao(dados_base, key=lambda p: p.idade)
        t_d = medir_tempo_execucao(dados_base, key=lambda p: p.idade, reverse=True)
        resultados_pessoas["crescente"].append(t_c)
        resultados_pessoas["decrescente"].append(t_d)
        print(f"{n:>7} -> crescente: {t_c:.2f} ms | decrescente: {t_d:.2f} ms")

    gerar_graficos(tamanhos, resultados_pessoas, "Shell Sort - Objetos (Pessoa.idade)", "shellsort_pessoas.png")

    print("\n✔ Gráficos gerados e exibidos com sucesso!")


# 7. DEMONSTRAÇÃO INTERATIVA


def demonstracao():
    print(" DEMONSTRAÇÃO DO SHELL SORT ")
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
    print("\n Demonstração concluida")


# 8. MENU ORIGINAL


if __name__ == "__main__":
    while True:
        print("\n MENU SHELL SORT ")
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
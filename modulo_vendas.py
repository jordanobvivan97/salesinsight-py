"""
modulo_vendas.py
Funções do pipeline SalesInsight PY (somente biblioteca padrão do Python).
"""

import csv
import json
import os
import random

CAMPOS_OBRIGATORIOS = ["id_venda", "data_venda", "cliente", "produto",
                       "categoria", "regiao", "quantidade", "preco_unitario"]


# ---------------------------------------------------------------------------
# RF01 - Criar o dataset sintético
# ---------------------------------------------------------------------------
def gerar_dataset_sintetico(caminho_arquivo="vendas.csv", n_registros=150, seed=42):
    """Gera um CSV de vendas com sujeira proposital (nulos e espaços extras)."""
    random.seed(seed)  # mesma seed = mesmo dataset sempre (reprodutível)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    categorias = {"Notebook": "Eletrônicos", "Smartphone": "Celulares",
                  "Tablet": "Celulares", "Monitor": "Eletrônicos",
                  "Teclado": "Acessórios", "Mouse": "Acessórios"}
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

    dados = []
    for i in range(1, n_registros + 1):
        prod = random.choice(produtos)
        # ~5% de quantidades e preços vazios (nulos)
        qtd = str(random.randint(1, 8)) if random.random() > 0.05 else ""
        preco = str(round(random.uniform(100, 3500), 2)) if random.random() > 0.05 else ""
        # ~10% dos nomes de produto com espaços sobrando
        prod_nome = f"  {prod} " if random.random() < 0.1 else prod

        dados.append([
            i,
            f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            f"Cliente_{random.randint(1, 30):03d}",
            prod_nome,
            categorias.get(prod, "Outros"),
            random.choice(regioes),
            qtd,
            preco,
        ])

    with open(caminho_arquivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CAMPOS_OBRIGATORIOS)
        # Correção: o exemplo do enunciado gravava dados[0] duas vezes.
        writer.writerows(dados)
    print(f"[OK] Dataset gerado em: {caminho_arquivo}")


# ---------------------------------------------------------------------------
# RF07 - Leitura do CSV com csv.DictReader
# ---------------------------------------------------------------------------
def carregar_csv(caminho_arquivo):
    """Lê o CSV e devolve uma lista de dicionários (uma linha = um dict)."""
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")

    dados = []
    with open(caminho_arquivo, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            dados.append(linha)
    print(f"[OK] {len(dados)} registros lidos de: {caminho_arquivo}")
    return dados

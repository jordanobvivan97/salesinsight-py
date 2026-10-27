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


# ---------------------------------------------------------------------------
# RF02 - Inspeção dos dados
# ---------------------------------------------------------------------------
def inspecionar_dados(dados):
    """Mostra total de registros, campos e quantas linhas têm valores vazios."""
    print("\n=== INSPEÇÃO INICIAL DOS DADOS ===")
    print(f"Total de registros carregados: {len(dados)}")
    if not dados:
        print("Nenhum registro encontrado.")
        return {"total_registros": 0, "linhas_incompletas": 0, "nulos_por_campo": {}}

    print(f"Campos disponíveis: {list(dados[0].keys())}")
    print(f"Exemplo do primeiro registro: {dados[0]}")

    nulos_por_campo = {}
    linhas_incompletas = 0
    for linha in dados:
        tem_nulo = False
        for campo, valor in linha.items():
            if valor is None or str(valor).strip() == "":
                nulos_por_campo[campo] = nulos_por_campo.get(campo, 0) + 1
                tem_nulo = True
        if tem_nulo:
            linhas_incompletas += 1

    print(f"Linhas com dados incompletos/nulos: {linhas_incompletas}")
    for campo, qtd in nulos_por_campo.items():
        print(f"  - {campo}: {qtd} valor(es) vazio(s)")

    return {"total_registros": len(dados),
            "linhas_incompletas": linhas_incompletas,
            "nulos_por_campo": nulos_por_campo}


# ---------------------------------------------------------------------------
# RF03 - Limpeza e tratamento
# ---------------------------------------------------------------------------
def limpar_dados(dados_brutos):
    """Remove espaços, descarta linhas inválidas e converte tipos."""
    dados_limpos = []
    removidos = 0

    for lin in dados_brutos:
        qtd_txt = (lin.get("quantidade") or "").strip()
        preco_txt = (lin.get("preco_unitario") or "").strip()

        # Validação de nulos/vazios
        if not qtd_txt or not preco_txt:
            removidos += 1
            continue

        try:
            qtd = int(qtd_txt)
            preco = float(preco_txt)
            if qtd <= 0 or preco <= 0:  # valores sem sentido de negócio
                raise ValueError("quantidade ou preço não positivo")

            dados_limpos.append({
                "id_venda": int(lin["id_venda"]),
                "data_venda": lin["data_venda"].strip(),
                "cliente": lin["cliente"].strip(),
                "produto": lin["produto"].strip(),
                "categoria": lin["categoria"].strip(),
                "regiao": lin["regiao"].strip(),
                "quantidade": qtd,
                "preco_unitario": preco,
            })
        except (ValueError, KeyError):
            removidos += 1

    print("\n=== RELATÓRIO DE LIMPEZA ===")
    print(f"Registros Válidos: {len(dados_limpos)} | Registros Removidos: {removidos}")
    return dados_limpos

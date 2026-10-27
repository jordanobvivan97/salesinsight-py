"""
main.py
Ponto de entrada do SalesInsight PY: orquestra o pipeline de ponta a ponta.
"""

import os
import modulo_vendas as mv

# Caminhos relativos à pasta deste arquivo (funciona de qualquer diretório)
PASTA_BASE = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(PASTA_BASE, "vendas.csv")
PASTA_SAIDA = os.path.join(PASTA_BASE, "outputs")


def main():
    print("=" * 60)
    print(" SALESINSIGHT PY - Pipeline de Processamento com Python Nativo")
    print("=" * 60)

    # 1. Gerar dataset sintético se não existir
    if not os.path.exists(ARQUIVO_DADOS):
        mv.gerar_dataset_sintetico(ARQUIVO_DADOS, n_registros=150)

    # 2. Leitura e inspeção
    dados_brutos = mv.carregar_csv(ARQUIVO_DADOS)
    mv.inspecionar_dados(dados_brutos)

    # 3. Limpeza e transformação
    dados_limpos = mv.limpar_dados(dados_brutos)
    dados_transformados = mv.criar_campos_derivados(dados_limpos)

    # 4. Função de ordem superior com lambda
    dados_com_tag = mv.processar_transformacao(
        dados_transformados,
        lambda x: {**x, "processado": True}
    )

    # 5. Métricas e segmentação
    metricas = mv.calcular_metricas(dados_com_tag)
    segmentos = mv.segmentar_clientes(dados_com_tag)
    top_clientes = mv.obter_top_clientes(segmentos, top_n=5)

    # 6. Resumo executivo
    print("\n=== RESUMO EXECUTIVO ===")
    print(f"Receita Total da Empresa: R$ {metricas['total_geral']:,.2f}")

    print("\nReceita por Categoria:")
    for cat, rec in metricas["por_categoria"].items():
        print(f"  - {cat}: R$ {rec:,.2f}")

    print("\nReceita por Região:")
    for reg, rec in metricas["por_regiao"].items():
        print(f"  - {reg}: R$ {rec:,.2f}")

    print("\nTop 5 Clientes Ouro/Prata:")
    for cli, info in top_clientes:
        print(f"  - {cli}: R$ {info['total_gasto']:,.2f} ({info['segmento']})")

    # 7. Exportação
    mv.exportar_resultados(metricas, segmentos, PASTA_SAIDA)

    print("\n[CONCLUÍDO] Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()

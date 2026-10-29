# SalesInsight PY - Pipeline de Análise de Dados de Vendas

Pipeline simples e modularizado para tratamento, transformação e agregação de dados de vendas utilizando apenas recursos nativos do Python (`csv`, `json`, `os`, `random`).

## Estrutura do Projeto

- `main.py`: ponto de entrada; importa o módulo e executa o pipeline.
- `modulo_vendas.py`: funções de geração, leitura, inspeção, limpeza, transformação, agregação, segmentação e exportação.
- `vendas.csv`: dataset sintético de vendas (150 registros, com nulos e espaços propositais).
- `outputs/`: relatórios gerados (`metricas_resumo.csv` e `estatisticas.json`).

## Como Executar

1. Tenha o Python 3 instalado.
2. Clone ou descompacte o repositório.
3. No terminal, dentro da pasta do projeto, execute:

```bash
python main.py
```

Se `vendas.csv` não existir, ele é gerado automaticamente (seed 42, resultado reprodutível).

## Etapas do Pipeline

| Etapa | Função | O que faz |
|---|---|---|
| RF01 | `gerar_dataset_sintetico` | Cria o CSV com dados sintéticos |
| RF07 | `carregar_csv` | Lê o CSV com `csv.DictReader` |
| RF02 | `inspecionar_dados` | Total de registros e contagem de nulos por campo |
| RF03 | `limpar_dados` | `.strip()`, remove linhas vazias/inválidas, converte para `int`/`float` |
| RF04 | `criar_campos_derivados` | Cria `receita_total` e `faixa_preco` |
| Extra | `processar_transformacao` | Função de ordem superior aplicada com `lambda` |
| RF05 | `calcular_metricas` | Receita por categoria, por região e total geral |
| RF06 | `segmentar_clientes` / `obter_top_clientes` | Bronze, Prata, Ouro e ranking |
| RF07 | `exportar_resultados` | Exporta JSON e CSV em `outputs/` |

## Decisões de Implementação

- **faixa_preco**: classificada pela `receita_total` (quantidade × preço), seguindo o código de exemplo do enunciado: Baixo (< R$ 500), Médio (R$ 500 a R$ 2.000), Alto (> R$ 2.000).
- **Segmentação**: Bronze (< R$ 3.000), Prata (R$ 3.000 a R$ 8.000), Ouro (> R$ 8.000).
- **Distribuição dos segmentos**: com o gerador do enunciado (30 clientes, preços até R$ 3.500 e até 8 unidades por venda), quase todos os clientes passam de R$ 8.000 e caem em Ouro. A regra de classificação está correta; a concentração vem do volume do dataset sintético.
- **Correção do gerador**: o exemplo do enunciado gravava o primeiro registro duas vezes; a linha duplicada foi removida.
- **Caminhos relativos**: os arquivos são localizados a partir da pasta do `main.py`, sem caminhos absolutos.

## Versionamento

Cada funcionalidade foi desenvolvida em uma branch própria (`feat/...`) e mesclada na `main`. Veja o histórico com:

```bash
git log --oneline --graph --all
```

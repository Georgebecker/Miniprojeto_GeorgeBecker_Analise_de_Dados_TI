"""Limpa a base de varejo e apresenta estatísticas e padrões dos pedidos."""

from pathlib import Path

import pandas as pd
import numpy as np

PASTA_PROJETO = Path(__file__).resolve().parent
ARQUIVO_CSV = PASTA_PROJETO / "Base Varejo.csv"
ARQUIVO_COMPACTADO = PASTA_PROJETO / "Bdados" / "Base Varejo.csv.zip"
ARQUIVO_LIMPO = PASTA_PROJETO / "df_limpo.csv"

print("--- INICIANDO A ANÁLISE EXPLORATÓRIA DE DADOS (AED) - VAREJO ---")

if ARQUIVO_CSV.exists():
    # Primeiro tentamos o CSV já extraído; assim o script também funciona com a
    # forma de arquivo indicada no enunciado e não depende da pasta atual do terminal.
    df = pd.read_csv(ARQUIVO_CSV, sep=";", encoding="utf-8")
elif ARQUIVO_COMPACTADO.exists():
    # Como abrir um pacote sem desempacotá-lo: o pandas lê o único CSV dentro do ZIP.
    df = pd.read_csv(ARQUIVO_COMPACTADO, sep=";", encoding="utf-8", compression="zip")
else:
    print(
        "Erro: não encontrei 'Base Varejo.csv' na pasta do projeto nem "
        "'Bdados\\Base Varejo.csv.zip'. Confira os arquivos de dados."
    )
    raise SystemExit(1)

print("\n[1] DADOS CARREGADOS COM SUCESSO!")
print(f"-> Registros: {df.shape[0]} | Colunas: {df.shape[1]}")
print("\n-> Tipos de dados originais:")
print(df.dtypes)

# Uma limpeza é como organizar uma planilha antes de fazer as contas:
# primeiro removemos colunas sem conteúdo útil e padronizamos os valores ausentes.
print("\n" + "="*50)
print("DIAGNÓSTICO E LIMPEZA DE DADOS")
print("="*50)

# A base recebida pode ter quatro colunas extras vazias; filtramos somente as
# que realmente existirem para o script continuar compatível com versões diferentes.
colunas_lixo = ['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13']
df = df.drop(columns=[c for c in colunas_lixo if c in df.columns])

# Marcadores escritos como texto passam a ser valores ausentes reconhecidos pelo pandas.
df = df.replace({'#N/D': np.nan, 'NULL': np.nan, 'N/A': np.nan})

def tratar_categoria(cat):
    """Preenche categorias ausentes e padroniza as demais para facilitar agrupamentos."""
    if pd.isna(cat) or str(cat).strip() == '' or str(cat) == '#N/D':
        return 'Sem Categoria'
    else:
        return str(cat).strip().title()

df['PR_CAT'] = df['PR_CAT'].apply(tratar_categoria)

# Sem o nome, não é possível identificar o item em uma análise detalhada; por isso,
# removemos essas linhas, mas mantemos pedidos que tenham outros itens identificáveis.
nulos_antes = len(df)
df = df.dropna(subset=['PR_NOME'])
print(f"-> Registros sem nome de produto removidos: {nulos_antes - len(df)}")

# CO_ID pode aparecer em várias linhas porque um pedido pode conter vários produtos.
# Excluir essas linhas apagaria itens legítimos; os agrupamentos contam pedidos com
# nunique(), sem confundir linhas de produto com compras diferentes.
print(f"-> Pedidos distintos preservados: {df['CO_ID'].nunique()}")
print(f"-> Linhas de produtos preservadas: {len(df)}")

# A data chega como texto. A conversão funciona como conferir cada data de um
# calendário: valores impossíveis viram ausentes e são retirados antes da análise.
df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')
datas_invalidas = df['DATA'].isnull().sum()
df = df.dropna(subset=['DATA'])
print(f"-> Datas inválidas (ex: 30/02) removidas: {datas_invalidas}")

# Após remover linhas, reorganizamos a numeração para não deixar lacunas.
df = df.reset_index(drop=True)

# Valores como "2" precisam ser números para calcular média e quartis.
# Qualquer conteúdo que não possa ser convertido vira ausente, não um número inventado.
df['CL_FHL'] = pd.to_numeric(df['CL_FHL'], errors='coerce')

# O arquivo exportado contém os dados já limpos e com CL_FHL numérico.
df.to_csv(ARQUIVO_LIMPO, index=False, sep=';')
print(f"\n-> Arquivo '{ARQUIVO_LIMPO.name}' exportado com sucesso na pasta do projeto!")

print("\n" + "="*50)
print("ESTATÍSTICAS DESCRITIVAS: NÚMERO DE FILHOS (CL_FHL)")
print("="*50)

# CL_FHL descreve o cliente e aparece repetido nas linhas de produtos. Agrupar
# por CL_ID evita dar mais peso a quem fez pedidos com mais itens.
valores_filhos = df.groupby('CL_ID')['CL_FHL'].first().dropna()
if valores_filhos.empty:
    print("Não há valores numéricos válidos para calcular as estatísticas.")
    media_filhos = mediana_filhos = None
else:
    moda_filhos = valores_filhos.mode()
    media_filhos = valores_filhos.mean()
    mediana_filhos = valores_filhos.median()
    print(f"Média: {media_filhos:.2f}")
    print(f"Mediana: {mediana_filhos:.2f}")
    print(f"Desvio Padrão: {valores_filhos.std():.2f}")
    print(f"Moda: {moda_filhos.iloc[0]:g}")
    print(f"Máximo: {valores_filhos.max():g}")
    print(f"Mínimo: {valores_filhos.min():g}")
    print(f"Contagem (Clientes com valor válido): {valores_filhos.count()}")
    print("\nQuartis (25%, 50%, 75%):")
    print(valores_filhos.quantile([0.25, 0.5, 0.75]))

print("\n" + "="*50)
print("PADRÕES DE AGRUPAMENTO (INSIGHTS)")
print("="*50)

# nunique conta cada pedido uma vez, mesmo quando ele possui vários produtos.
print("\n-> Volume de Compras por Gênero (CL_GENERO):")
vendas_genero = df.groupby('CL_GENERO')['CO_ID'].nunique().sort_values(ascending=False)
print(vendas_genero)
genero_lider = vendas_genero.index[0] if not vendas_genero.empty else "não disponível"

# Uma compra pode conter produtos de várias categorias; o total por categoria
# representa pedidos que incluem a categoria, não faturamento nem unidades vendidas.
print("\n-> Top 5 categorias presentes em mais pedidos (PR_CAT):")
vendas_categoria = df.groupby('PR_CAT')['CO_ID'].nunique().sort_values(ascending=False).head(5)
print(vendas_categoria)
categoria_lider = vendas_categoria.index[0] if not vendas_categoria.empty else "não disponível"

print("\n" + "="*50)
print("CONCLUSÕES FINAIS E INSIGHTS")
print("="*50)
print("1. Qualidade dos Dados: colunas extras foram removidas, categorias ausentes foram identificadas e linhas sem nome de produto ou data válida foram descartadas.")
print(f"2. Público por gênero: {genero_lider} apresentou o maior número de pedidos distintos.")
print(f"3. Categorias: {categoria_lider} foi a categoria presente em mais pedidos distintos.")
if media_filhos is None:
    print("4. Perfil familiar: não foi possível calcular média e mediana de CL_FHL.")
else:
    print(f"4. Perfil familiar: média de {media_filhos:.2f} filho(s) e mediana de {mediana_filhos:.2f}.")
print("5. Oportunidade: os resultados indicam quais grupos e categorias merecem investigação; contagem de pedidos, sozinha, não mede faturamento nem retorno de campanha.")
print("="*50)
print("ANÁLISE CONCLUÍDA COM SUCESSO!")
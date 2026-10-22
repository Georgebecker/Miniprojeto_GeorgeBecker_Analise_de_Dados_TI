# Mini-Projeto Avaliativo - Módulo 1

**Aluno:** George Herman Becker
**Turma:** Analise_de_Dados_TI
**Base de Dados:** Base Varejo (Kaggle) Base Varejo.csv.zip

## 1. Contextualização e Objetivo

Este projeto consiste no desenvolvimento de uma Análise Exploratória de Dados (AED) aplicada ao setor de varejo. O objetivo principal é executar um pipeline de ETL (Extração, Transformação e Carga) para tratar inconsistências na base de dados, realizar a limpeza necessária e extrair métricas operacionais e insights de negócio que possam apoiar a tomada de decisão.

## 2. Reflexão Teórica sobre ETL e Qualidade de Dados

Durante o desenvolvimento do script, a etapa de Transformação exigiu a tomada de decisões fundamentadas nos princípios de qualidade de dados:

*   **Tratamento de Categorias Vazias:** Foi implementada uma estrutura condicional (`if/else`) para preencher categorias de produtos que estavam nulas, vazias ou com códigos de erro (como `#N/D`) com o rótulo "Sem Categoria". Essa escolha garante que o volume de vendas não seja descartado por falhas de cadastro, preservando a integridade da contagem de pedidos.
*   **Tratamento de Nulos em Dimensões Físicas:** Para a coluna de nome do produto (`PR_NOME`), a decisão foi remover as linhas com valores nulos. A justificativa é que um registro de compra sem a descrição do produto perde seu valor analítico granular. Como a categoria do produto já foi preservada na etapa anterior, a remoção não compromete a análise macro.
*   **Identificação de pedidos:** A base possui várias linhas com o mesmo `CO_ID` porque um pedido pode incluir vários produtos. Remover essas linhas descartaria itens legítimos; por isso, o script preserva as linhas e usa `nunique()` para contar cada pedido apenas uma vez nos agrupamentos. Após a limpeza, a base contém 826.350 linhas de produtos e 18.469 pedidos distintos.
*   **Conversão de Tipos (Datas):** A coluna `DATA` foi convertida de texto para o tipo `datetime` utilizando a função `pd.to_datetime`. Datas inválidas (como 30/02) foram convertidas para nulas e posteriormente removidas, assegurando a consistência para futuras análises temporais.
*   **Exportação dos Dados:** Ao final do processo de limpeza, a base tratada foi exportada no formato `df_limpo.csv`, conforme exigido nas etapas do projeto.

## 3. Principais Insights Obtidos

A partir das estatísticas descritivas e dos agrupamentos realizados, destacam-se os seguintes pontos:

1.  **Qualidade dos Dados:** O script remove as colunas extras e as linhas sem nome de produto, padroniza categorias e descarta datas inválidas. As várias linhas de um mesmo `CO_ID` são preservadas para não apagar produtos do pedido.
2.  **Liderança por Gênero:** O gênero **F** aparece em 9.614 pedidos distintos, contra 8.855 do gênero **M**.
3.  **Categorias com mais pedidos:** **Alimentos** está presente em 18.267 pedidos distintos, seguido por Higiene (17.610) e Limpeza (17.475). Essa contagem indica presença em pedidos, não faturamento ou unidades vendidas.
4.  **Perfil Familiar (Número de Filhos):** Na coluna `CL_FHL`, calculada uma vez por cliente, a média é **1,14** e a mediana é **0** filho(s). A mediana igual a zero indica que pelo menos metade dos clientes válidos tem valor zero.
5.  **Oportunidade de Negócio:** Alimentos é uma categoria a investigar em análises futuras. A contagem de pedidos, isoladamente, não permite estimar faturamento nem retorno de campanhas.

## 4. Instruções de Execução

1.  Abra o PowerShell na pasta do projeto ou siga os passos em [`COMANDOS_TERMINAL.txt`](COMANDOS_TERMINAL.txt).
2.  Os comandos criam um ambiente virtual, instalam `pandas` e `numpy` e executam o script.
3.  O script usa `Bdados/Base Varejo.csv.zip`, já incluído no projeto. Também aceita `Base Varejo.csv` extraído na pasta principal.
4.  O terminal exibirá o diagnóstico, as estatísticas e os agrupamentos; o arquivo `df_limpo.csv` será gerado na pasta principal.
# Contexto para IA

## Visão geral

Este documento descreve duas tabelas independentes de produção assistencial do SUS/DATASUS:

1. **`public.internacoes`**: registros hospitalares de internação, em que cada linha representa uma AIH (Autorização de Internação Hospitalar).
2. **`public.atendimentos_ambulatorial`**: registros ambulatoriais, em que cada linha representa um atendimento/procedimento ambulatorial. Essa tabela não possui um identificador único padronizado por registro e pode incluir consultas, exames, procedimentos clínicos, cirúrgicos, medicamentos, OPME e outros atendimentos.

As tabelas devem ser analisadas separadamente, pois representam naturezas assistenciais distintas: internações hospitalares versus produção ambulatorial.

---

## Tabela `public.internacoes`

Cada registro representa uma **AIH (Autorização de Internação Hospitalar)**, documento administrativo usado pelo SUS para autorizar, identificar e controlar uma internação hospitalar. A AIH possui número próprio, identifica a internação e está associada a informações do paciente, procedimento, diagnóstico, unidade de saúde, datas e faturamento.

### Unidade de análise

- **Uma linha = uma AIH / uma internação hospitalar.**
- O identificador principal da internação é **`N_AIH`**.

### Campos principais

#### Identificação da internação

- **`N_AIH`**: número/código da AIH. Identifica de forma única a internação hospitalar na base.

#### Paciente

- **`PACIENTE_RESIDENCIA_MUNICIPIO`**: município de residência do paciente.
- **`PACIENTE_RESIDENCIA_REGIAO`**: região de saúde de residência do paciente.
- **`PACIENTE_RESIDENCIA_MACRORREGIAO`**: macrorregião de saúde de residência do paciente.
- **`PACIENTE_RESIDENCIA_ESTADO`**: estado de residência do paciente.
- **`PACIENTE_IDADE`**: idade do paciente, em anos, no momento da internação.
- **`PACIENTE_OBITO`**: indicador binário de óbito na internação. `0` = não faleceu; `1` = faleceu.

#### Procedimento

- **`PROCEDIMENTO_CODIGO`**: código do procedimento hospitalar conforme tabela oficial DATASUS/SUS.
- **`PROCEDIMENTO_DESCRICAO`**: descrição textual do procedimento realizado.

#### Diagnóstico

- **`CID_CODIGO`**: código CID associado à internação.
- **`CID_DESCRICAO`**: descrição textual do diagnóstico CID.

#### Datas

- **`DATA_INTERNACAO`**: data de admissão hospitalar.
- **`DATA_SAIDA`**: data de alta, saída, transferência ou óbito.

#### Unidade de saúde

- **`UNIDADE_SAUDE_CNES`**: código CNES da unidade em que a internação ocorreu.
- **`UNIDADE_SAUDE_NOME_FANTA`**: nome fantasia da unidade de saúde.
- **`UNIDADE_SAUDE_MUNICIPIO`**: município da unidade de saúde.
- **`UNIDADE_SAUDE_REGIAO`**: região de saúde da unidade.
- **`UNIDADE_SAUDE_MACRORREGIAO`**: macrorregião de saúde da unidade.
- **`UNIDADE_SAUDE_ESTADO`**: estado da unidade de saúde.

#### Faturamento e permanência

- **`QT_DIARIAS`**: quantidade de diárias da internação.
- **`VAL_TOT`**: valor total faturado da internação, em reais.

---

## Tabela `public.atendimentos_ambulatorial`

Cada registro representa um **atendimento/procedimento ambulatorial**. A base não é composta apenas por consultas: também pode conter exames, procedimentos diagnósticos, procedimentos clínicos, cirúrgicos, medicamentos, OPME, transplantes e outras produções ambulatoriais. O tipo de atendimento deve ser inferido principalmente pelos campos de procedimento.

### Unidade de análise

- **Uma linha = um atendimento/procedimento ambulatorial.**
- A tabela **não possui um identificador único padronizado equivalente ao `N_AIH`**.
- Para distinguir consultas, exames e outros tipos de produção, use principalmente **`PROCEDIMENTO_CODIGO`**, **`PROCEDIMENTO_DESCRICAO`**, **`PROCEDIMENTO_GRUPO`** e **`PROCEDIMENTO_SUBGRUPO`**.

### Campos principais

#### Paciente

- **`PACIENTE_RESIDENCIA_MUNICIPIO`**: município de residência do paciente.
- **`PACIENTE_RESIDENCIA_REGIAO`**: região de saúde de residência do paciente.
- **`PACIENTE_RESIDENCIA_MACRORREGIAO`**: macrorregião de saúde de residência do paciente.
- **`PACIENTE_RESIDENCIA_ESTADO`**: estado de residência do paciente.
- **`PACIENTE_IDADE`**: idade do paciente, em anos, no momento do atendimento.
- **`PACIENTE_OBITO`**: indicador binário de óbito relacionado ao atendimento. `0` = não foi a óbito; `1` = faleceu.

#### Procedimento

- **`PROCEDIMENTO_CODIGO`**: código do procedimento ambulatorial conforme tabela oficial DATASUS/SUS. Ajuda a identificar se o registro corresponde a consulta, exame ou outro atendimento.
- **`PROCEDIMENTO_DESCRICAO`**: descrição textual do procedimento ambulatorial. Também ajuda a interpretar o tipo de atendimento.
- **`PROCEDIMENTO_GRUPO`**: classificação macro do procedimento. Útil para separar tipos de produção ambulatorial, como procedimentos clínicos, procedimentos diagnósticos, medicamentos, procedimentos cirúrgicos, OPME e transplantes.
- **`PROCEDIMENTO_SUBGRUPO`**: classificação mais detalhada dentro do grupo. Deve ser priorizada quando a pergunta mencionar um tipo específico de exame ou procedimento, como tomografia, ultrassonografia, laboratório clínico, teste rápido, radiologia ou ressonância magnética.
- **`PERIODO_PROCEDIMENTO`**: data do procedimento ambulatorial.

### Interpretação analítica de grupos e subgrupos

- Quando **`PROCEDIMENTO_GRUPO` = `Procedimentos com finalidade diagnóstica`**, interprete o registro, em geral, como **exame**.
- Para exames, use **`PROCEDIMENTO_SUBGRUPO`** para classificar o tipo:
  - Subgrupos de **laboratório/hemoterapia/anatomia patológica/coleta/teste rápido/vigilância** tendem a ser exames **laboratoriais**.
  - Subgrupos de **radiologia, tomografia, ressonância magnética, ultrassonografia, endoscopia, medicina nuclear e radiologia intervencionista** tendem a ser exames de **imagem**.
  - **Métodos diagnósticos em especialidades** deve ser tratado como categoria mista ou inespecífica, salvo detalhamento adicional.

#### Diagnóstico

- **`CID_CODIGO`**: código CID associado ao atendimento ambulatorial.
- **`CID_DESCRICAO`**: descrição textual do diagnóstico CID.

#### Unidade de saúde

- **`UNIDADE_SAUDE_CNES`**: código CNES da unidade em que o atendimento ocorreu.
- **`UNIDADE_SAUDE_NOME_FANTA`**: nome fantasia da unidade de saúde.
- **`UNIDADE_SAUDE_MUNICIPIO`**: município da unidade de saúde.
- **`UNIDADE_SAUDE_REGIAO`**: região de saúde da unidade.
- **`UNIDADE_SAUDE_MACRORREGIAO`**: macrorregião de saúde da unidade.
- **`UNIDADE_SAUDE_ESTADO`**: estado da unidade de saúde.

#### Faturamento

- **`VAL_TOT`**: valor total faturado do atendimento/procedimento ambulatorial, em reais.

---

## Observações gerais para consultas SQL e análises

- As tabelas são independentes e não devem ser unificadas sem critério explícito.
- Códigos como AIH, procedimento, CID e CNES podem estar armazenados como texto numérico; evite remover zeros à esquerda.
- Datas podem precisar de conversão para `date`, por exemplo com `::date`.
- Valores textuais podem aparecer com diferenças de acentuação, capitalização ou grafia; use normalização quando necessário.
- Para análises geográficas, diferencie residência do paciente (`PACIENTE_RESIDENCIA_*`) da localização da unidade de saúde (`UNIDADE_SAUDE_*`).
- Para análises de custo, use `VAL_TOT`; em internações, `QT_DIARIAS` também permite analisar permanência hospitalar.
- Em internações, a contagem de registros equivale à contagem de AIHs/internações. Em ambulatorial, a contagem de registros equivale à contagem de atendimentos/procedimentos registrados.

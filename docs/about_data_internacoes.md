
# Contexto para IA

## Sobre os dados: Internações

Os dados de internações foram armazenados na tabela "public.internacoes". Cada registro nessa base de dados de internação é composto por uma AIH (Autorização de Internação Hospitalar), o registro utilizado pelo Sistema Único de Saúde para autorizar, identificar e controlar cada internação hospitalar realizada em unidades públicas ou conveniadas. A AIH associa-se a um documento administrativo que consolida informações essenciais sobre o paciente e sobre a internação realizada. Cada AIH possui um número único que identifica a internação e um código de procedimento vinculado à tabela oficial do DATASUS, garantindo padronização na produção hospitalar em nível nacional. Essa estrutura permite processamento correto dos dados para fins de faturamento, auditoria, acompanhamento assistencial e geração de indicadores de gestão.

### Informações do Paciente
- **N_AIH**: Na base de dados a coluna N_AIH contém o código/número AIH (Autorização de Internação Hospitalar) que é o registro utilizado pelo Sistema Único de Saúde para autorizar, identificar e controlar cada internação hospitalar realizada em unidades públicas ou conveniadas ao sistema de saúde. Esse código está associado a um documento administrativo denominado de AIH, que consolida todas as informações essenciais da internação, incluindo os dados do paciente, estabelecimento de saúde responsável. Vale ressaltar que nessa base de dados cada registro representa uma AIH identificada pelo N_AIH.
- **PACIENTE_RESIDENCIA_MUNICIPIO**: Município de residência do paciente. Campo de texto indicando a localização geográfica (cidade) onde o paciente reside, utilizado para análises de origem geográfica e padrões regionais de internação.
- **PACIENTE_RESIDENCIA_REGIAO**: Região de saúde de residência do paciente. Campo de texto que especifica a regionalização conforme divisão administrativa de saúde do estado, permitindo análises de demanda regional.
- **PACIENTE_RESIDENCIA_MACRORREGIAO**: Macrorregião de saúde de residência do paciente. Campo de texto indicando a divisão de macro-regiões conforme estrutura administrativa estadual, possibilitando análises em escala regional ampliada.
- **PACIENTE_RESIDENCIA_ESTADO**: Estado brasileiro de residência do paciente. Campo de texto identificando a unidade federativa onde o paciente reside.
- **PACIENTE_IDADE**: Idade do paciente (em anos) no momento da internação. Campo numérico essencial para análises demográficas, estratificação por faixa etária e indicadores epidemiológicos.
- **PACIENTE_OBITO**: Indicador de desfecho fatal da internação. Campo binário onde 0 = paciente teve alta/saída hospitalar vivo e 1 = paciente faleceu durante a internação, utilizado para cálculos de mortalidade e análises de risco.

### Informações do Procedimento
- **PROCEDIMENTO_CODIGO**: Código único do procedimento médico vinculado à tabela oficial DATASUS. Campo numérico que identifica de forma padronizada o procedimento realizado durante a internação, essencial para rastreabilidade, faturamento e indicadores assistenciais em nível nacional.
- **PROCEDIMENTO_DESCRICAO**: Descrição textual do procedimento médico. Campo de texto contendo o nome e detalhes clínicos do procedimento realizado, facilitando interpretação e análises de padrões de atendimento.

### Informações de Diagnóstico
- **CID_CODIGO**: Código de diagnóstico CID (Classificação Internacional de Doenças). Campo de texto contendo o código padronizado internacionalmente que identifica de forma única a doença, transtorno ou condição de saúde do paciente no momento da internação, essencial para rastreabilidade clínica, faturamento e geração de indicadores epidemiológicos em nível nacional e internacional.
- **CID_DESCRICAO**: Descrição textual do código de diagnóstico CID. Campo de texto contendo o nome clínico e detalhes da doença ou condição de saúde associada ao código CID, facilitando interpretação, análises de padrões de morbidade e correlações entre diagnósticos e desfechos clínicos da internação.

### Datas de Internação
- **DATA_INTERNACAO**: Data e hora de admissão hospitalar. Campo de data/hora que registra o momento exato (data e horário) em que o paciente foi admitido na unidade de saúde, essencial para cálculos de duração da internação, análises temporais, auditoria de registros e indicadores de gestão operacional.
- **DATA_SAIDA**: Data e hora de alta ou saída hospitalar. Campo de data/hora que registra o momento exato (data e horário) em que o paciente recebeu alta, foi transferido ou faleceu, utilizado para determinação do tempo de permanência, análises de fluxo de pacientes, faturamento e indicadores assistenciais.

### Unidade de Saúde
- **UNIDADE_SAUDE_CNES**: Identificador único CNES (Código Nacional de Estabelecimentos de Saúde). Trata-se de um código numérico padronizado que identifica de forma única o estabelecimento de saúde (hospital, clínica ou centro de atendimento) em que o paciente foi internado. Este código é utilizado pelo Sistema Único de Saúde para registros administrativos e de faturamento.
- **UNIDADE_SAUDE_NOME_FANTA**: Nome fantasia ou comercial da unidade de saúde. Campo de texto contendo a denominação popular ou comercial do estabelecimento, facilitando a identificação e referência ao hospital ou instituição de saúde responsável pela internação.
- **UNIDADE_SAUDE_MUNICIPIO**: Município onde a unidade de saúde está localizada. Campo de texto indicando a cidade em que o estabelecimento de saúde está registrado e onde a internação foi realizada.
- **UNIDADE_SAUDE_REGIAO**: Região de saúde onde a unidade de saúde está localizada. Campo de texto que especifica a regionalização geográfica conforme divisão administrativa de saúde do estado onde o estabelecimento opera.
- **UNIDADE_SAUDE_MACRORREGIAO**: Macro-região de saúde onde a unidade de saúde está localizada. Campo de texto indicando a divisão de macro-regiões conforme estrutura administrativa de saúde estadual, permitindo análises em escala regional mais ampla.
- **UNIDADE_SAUDE_ESTADO**: Estado brasileiro onde a unidade de saúde está localizada. Campo de texto identificando a unidade federativa em que o estabelecimento de saúde opera e onde a internação foi processada.

### Informações de Faturamento
- **QT_DIARIAS**: Quantidade de dias da internação hospitalar. Campo numérico representando a duração total do período de internação, calculado entre a data de admissão e a data de alta/saída, essencial para análises de tempo de permanência e custo operacional.
- **VAL_TOT**: Valor total da internação em reais (R$). Campo numérico contendo o custo total faturado pelo estabelecimento de saúde referente à internação, incluindo procedimentos, materiais e diárias. Utilizado para análises de custos, auditoria financeira e indicadores de gestão econômica do sistema de saúde.

## Sobre os dados: Consultas

Os dados de consultas estão armazenados na tabela "public.atendimentos_ambulatorial". Diferentemente dos dados de internação, essa base não possui um identificador único padronizado para cada registro. Cada linha da tabela representa um atendimento ambulatorial realizado.

Ressalta-se que essa base não é composta exclusivamente por consultas, mas também inclui exames e outros tipos de atendimentos ambulatoriais. A identificação do tipo de atendimento realizado ocorre por meio da interpretação do código do procedimento associado a cada registro, conforme padronização definida nas tabelas oficiais.

### Informações do Paciente

- **PACIENTE_RESIDENCIA_MUNICIPIO**: Município de residência do paciente. Campo de texto indicando a localização geográfica (cidade) onde o paciente reside.

- **PACIENTE_RESIDENCIA_REGIAO**: Região de saúde de residência do paciente. Campo de texto que especifica a regionalização conforme divisão administrativa de saúde do estado.

- **PACIENTE_RESIDENCIA_MACRORREGIAO**: Macrorregião de saúde de residência do paciente. Campo de texto indicando a divisão de macro-regiões conforme estrutura administrativa estadual.

- **PACIENTE_RESIDENCIA_ESTADO**: Estado brasileiro de residência do paciente. Campo de texto identificando a unidade federativa onde o paciente reside.

- **PACIENTE_IDADE**: Idade do paciente (em anos) no momento do atendimento. Campo numérico essencial para análises demográficas, estratificação por faixa etária e indicadores epidemiológicos.

- **PACIENTE_OBITO**: Indicador de desfecho fatal relacionado ao atendimento. Campo binário onde 0 = paciente não foi a óbito e 1 = paciente faleceu, utilizado para cálculos de mortalidade e análises de risco em contexto ambulatorial.

### Informações do Procedimento

- **PROCEDIMENTO_CODIGO**: Código único do procedimento ambulatorial vinculado à tabela oficial DATASUS. Campo de texto que identifica de forma padronizada o procedimento realizado durante o atendimento, essencial para rastreabilidade, faturamento e indicadores assistenciais em nível nacional. Esse campo que irá identificar por exemplo se esse procedimento trata-se de uma consulta ou exame.

- **PROCEDIMENTO_DESCRICAO**: Descrição textual do procedimento ambulatorial. Campo de texto contendo o nome e detalhes clínicos do procedimento realizado, facilitando interpretação e análises de padrões de atendimento. Esse campo que irá identificar por exemplo se esse procedimento trata-se de uma consulta ou exame.

- **PERIODO_PROCEDIMENTO**: Data do procedimento ambulatorial. Campo de data que indica quando o procedimento foi realizado.

### Informações de Diagnóstico

- **CID_CODIGO**: Código de diagnóstico CID (Classificação Internacional de Doenças). Campo de texto contendo o código padronizado internacionalmente que identifica de forma única a doença, transtorno ou condição de saúde do paciente no momento do atendimento, essencial para rastreabilidade clínica, faturamento e geração de indicadores epidemiológicos em nível nacional e internacional.

- **CID_DESCRICAO**: Descrição textual do código de diagnóstico CID. Campo de texto contendo o nome clínico e detalhes da doença ou condição de saúde associada ao código CID, facilitando interpretação, análises de padrões de morbidade e correlações entre diagnósticos e desfechos clínicos do atendimento ambulatorial.

### Unidade de Saúde

- **UNIDADE_SAUDE_CNES**: Identificador único CNES (Código Nacional de Estabelecimentos de Saúde). Código numérico padronizado que identifica de forma única o estabelecimento de saúde (hospital, clínica, UBS ou centro de atendimento) onde o atendimento ambulatorial foi realizado, utilizado pelo SUS para registros administrativos e de faturamento.

- **UNIDADE_SAUDE_NOME_FANTA**: Nome fantasia ou comercial da unidade de saúde. Campo de texto contendo a denominação popular ou comercial do estabelecimento, facilitando a identificação e referência à unidade responsável pelo atendimento ambulatorial.

- **UNIDADE_SAUDE_MUNICIPIO**: Município onde a unidade de saúde está localizada. Campo de texto indicando a cidade em que o estabelecimento de saúde está registrado e onde o atendimento ambulatorial foi realizado.

- **UNIDADE_SAUDE_REGIAO**: Região de saúde onde a unidade de saúde está localizada. Campo de texto que especifica a regionalização geográfica conforme divisão administrativa de saúde do estado onde o estabelecimento opera.

- **UNIDADE_SAUDE_MACRORREGIAO**: Macro-região de saúde onde a unidade de saúde está localizada. Campo de texto indicando a divisão de macro-regiões conforme estrutura administrativa de saúde estadual, permitindo análises em escala regional mais ampla.

- **UNIDADE_SAUDE_ESTADO**: Estado brasileiro onde a unidade de saúde está localizada. Campo de texto identificando a unidade federativa em que o estabelecimento de saúde opera e onde o atendimento ambulatorial foi processado.

### Informações de Faturamento

- **VAL_TOT**: Valor total do atendimento ambulatorial em reais (R$). Campo numérico contendo o custo total faturado pelo estabelecimento de saúde referente ao procedimento realizado. Utilizado para análises de custos, auditoria financeira e indicadores de gestão econômica do sistema de saúde.

## Exemplos reais de registros (amostra)

Use estes exemplos para inferir tipos e padrões de preenchimento.
- Datas podem vir como texto e devem ser convertidas com `::date` quando necessário.
- Códigos (AIH, procedimento, CID, CNES) podem vir como texto numérico.
- Valores textuais podem vir com ou sem acento e em diferentes capitalizações.

### Exemplo 1
N_AIH: 5225105220654  
PACIENTE_RESIDENCIA_MUNICIPIO: Valparaíso de Goiás  
PACIENTE_RESIDENCIA_REGIAO: Região Centro-Oeste  
PACIENTE_RESIDENCIA_MACRORREGIAO: Nordeste  
PACIENTE_RESIDENCIA_ESTADO: GOIAS  
PACIENTE_IDADE: 18  
PACIENTE_OBITO: 0  
PROCEDIMENTO_CODIGO: 0308020030  
PROCEDIMENTO_DESCRICAO: TRATAMENTO DE INTOXICACAO OU ENVENENAMENTO POR EXPOSICAO A MEDICAMENTO E SUBSTANCIAS DE USO NAO MEDICINAL  
DATA_INTERNACAO: 2025-10-31  
DATA_SAIDA: 2025-10-31  
CID_CODIGO: F199  
CID_DESCRICAO: TRANSTORNOS MENTAIS E COMPORTAMENTAIS DEVIDOS AO USO DE MULTIPLAS DROGAS E AO USO DE OUTRAS SUBSTANCIAS PSICOATIVAS - TRANSTORNO MENTAL OU COMPORTAMENTAL NAO ESPECIFICADO  
UNIDADE_SAUDE_CNES: 6281303  
UNIDADE_SAUDE_NOME_FANTA: HOSPITAL MUNICIPAL DE VALPARAISO  
UNIDADE_SAUDE_MUNICIPIO: Valparaíso de Goiás  
UNIDADE_SAUDE_REGIAO: Região Centro-Oeste  
UNIDADE_SAUDE_MACRORREGIAO: Nordeste  
UNIDADE_SAUDE_ESTADO: GOIAS  
QT_DIARIAS: 1  
VAL_TOT: 144.95
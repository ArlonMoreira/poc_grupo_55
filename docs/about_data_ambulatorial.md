
# Contexto para IA

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

- **PROCEDIMENTO_GRUPO**: Classificação macro do procedimento ambulatorial conforme a tabela de grupos do SUS/DATASUS. Campo de texto que representa a natureza assistencial principal do atendimento realizado e ajuda a distinguir o tipo de produção ambulatorial (ex.: consulta, exame, cirurgia, dispensação de medicamento, transplante, etc.). Este campo é essencial para análises por perfil de atendimento, planejamento de oferta assistencial e avaliação de custos por grupo.

  Possíveis valores observados e interpretação analítica:
  - **Ações complementares da atenção à saúde**: procedimentos de suporte e complemento ao cuidado principal, incluindo atividades assistenciais acessórias necessárias para continuidade do tratamento.
  - **Ações de promoção e prevenção em saúde**: ações voltadas à prevenção de agravos, educação em saúde, rastreamento e intervenções de promoção da saúde.
  - **Medicamentos**: registros relacionados à dispensação/fornecimento de medicamentos no âmbito ambulatorial.
  - **Órteses, próteses e materiais especiais**: procedimentos associados à concessão ou uso de OPME, relevantes para análises de custo e complexidade assistencial.
  - **Procedimentos cirúrgicos**: intervenções cirúrgicas registradas no contexto ambulatorial.
  - **Procedimentos clínicos**: atendimentos e procedimentos clínicos não cirúrgicos, incluindo parte importante das consultas e condutas assistenciais ambulatoriais.
  - **Procedimentos com finalidade diagnóstica**: exames e procedimentos diagnósticos (laboratoriais, imagem e outros métodos diagnósticos). **Para fins analíticos, este grupo deve ser interpretado como "exames".**
  - **Transplantes de orgãos, tecidos e células**: atendimentos/procedimentos relacionados à linha de cuidado de transplantes no contexto ambulatorial.

- **PROCEDIMENTO_SUBGRUPO**: Classificação detalhada do procedimento ambulatorial dentro do grupo principal. Campo de texto usado para discriminar com maior precisão o tipo de exame/procedimento (por exemplo, tomografia, ultrassonografia, laboratório clínico, teste rápido). Esse campo deve ser priorizado quando a pergunta do usuário especificar o tipo de exame.

  Subgrupos observados e classificação analítica sugerida:
  - **Diagnóstico e procedimentos especiais em hemoterapia**: exames/procedimentos de medicina transfusional (tipagem sanguínea, compatibilidade, testes imuno-hematológicos e suporte hemoterápico). Classificação sugerida: **laboratorial**.
  - **Diagnóstico por ressonância magnética**: exame por imagem com campo magnético e radiofrequência, útil para avaliação detalhada de partes moles, sistema nervoso e estruturas osteoarticulares. Classificação sugerida: **imagem**.
  - **Diagnóstico por radiologia**: exames radiológicos convencionais (como raio-X) e variações diagnósticas com radiação ionizante para avaliação anatômica. Classificação sugerida: **imagem**.
  - **Diagnóstico em laboratório clínico**: exames laboratoriais de rotina e especializados (hematologia, bioquímica, microbiologia, imunologia, hormônios etc.). Classificação sugerida: **laboratorial**.
  - **Diagnóstico por tomografia**: tomografia computadorizada para análise em cortes anatômicos, amplamente usada em urgência e investigação de múltiplos sistemas. Classificação sugerida: **imagem**.
  - **Diagnóstico por endoscopia**: métodos diagnósticos com visualização interna de cavidades e órgãos por endoscópio, podendo incluir registro por imagem e coleta de material. Classificação sugerida: **imagem**.
  - **Diagnóstico por anatomia patológica e citopatologia**: análise microscópica de tecidos e células (biópsias e citologia), importante para confirmação diagnóstica, incluindo neoplasias. Classificação sugerida: **laboratorial**.
  - **Coleta de material**: procedimentos de coleta de amostras biológicas (sangue, secreções, tecidos e outros) para análise diagnóstica posterior. Classificação sugerida: **laboratorial**.
  - **Diagnóstico por medicina nuclear in vivo**: exames com radiofármacos para avaliação funcional e anatômica de órgãos, com forte componente de imagem funcional. Classificação sugerida: **imagem**.
  - **Diagnóstico em vigilância epidemiológica e ambiental**: exames e análises para monitoramento de agravos, surtos, agentes infecciosos e fatores ambientais de risco. Classificação sugerida: **laboratorial**.
  - **Diagnóstico por teste rápido**: testes de resposta rápida para triagem e apoio diagnóstico imediato, com leitura em curto prazo. Classificação sugerida: **laboratorial**.
  - **Métodos diagnósticos em especialidades**: categoria ampla que reúne métodos diagnósticos específicos por especialidade (cardiologia, neurologia, oftalmologia etc.), podendo incluir exames funcionais e de imagem. Classificação sugerida: **outros diagnósticos** (misto/inespecífico sem detalhamento adicional).
  - **Diagnóstico por ultrasonografia**: exame de imagem por ultrassom, sem radiação ionizante, usado para avaliação estrutural e, quando aplicável, fluxo vascular (Doppler). Classificação sugerida: **imagem**.
  - **Diagnóstico por radiologia intervencionista**: procedimentos diagnósticos minimamente invasivos guiados por imagem, frequentemente com maior complexidade técnica. Classificação sugerida: **imagem**.

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
- Códigos de procedimento podem ser numéricos em texto.
- Valores textuais podem vir com ou sem acento e em diferentes capitalizações.

### Exemplo 1
PACIENTE_RESIDENCIA_MUNICIPIO: Águas Lindas de Goiás  
PACIENTE_RESIDENCIA_REGIAO: Região Centro-Oeste  
PACIENTE_RESIDENCIA_MACRORREGIAO: Nordeste  
PACIENTE_RESIDENCIA_ESTADO: GOIAS  
PACIENTE_IDADE: 26  
PACIENTE_OBITO: 0  
PROCEDIMENTO_CODIGO: 0301060061  
PROCEDIMENTO_DESCRICAO: ATENDIMENTO DE URGENCIA EM ATENCAO ESPECIALIZADA  
PERIODO_PROCEDIMENTO: 2023-03-01  
CID_CODIGO: S626  
CID_DESCRICAO: FRATURA DE OUTROS DEDOS  
UNIDADE_SAUDE_CNES: 2442728  
UNIDADE_SAUDE_NOME_FANTA: HOSPITAL MUNICIPAL BOM JESUS  
UNIDADE_SAUDE_MUNICIPIO: Águas Lindas de Goiás  
UNIDADE_SAUDE_REGIAO: Região Centro-Oeste  
UNIDADE_SAUDE_MACRORREGIAO: Nordeste  
UNIDADE_SAUDE_ESTADO: GOIAS  
VAL_TOT: 0.0


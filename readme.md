# Projeto de Dashboard de Commodities

## Visão Geral
Este projeto consiste em um dashboard interativo para visualização de preços de commodities ao longo do tempo. Utilizando uma arquitetura moderna de dados, o projeto integra extração de dados financeiros, transformação com dbt (data build tool) e visualização através de uma aplicação web Streamlit.

## Estrutura do Projeto
```
dbt_classes/
├── app/                  # Aplicação Streamlit
│   └── app.py            # Código principal do dashboard
├── models/               # Modelos dbt
│   ├── staging/          # Modelos de staging
│   ├── intermediate/     # Modelos intermediários
│   └── marts/            # Modelos finais para consumo
├── analyses/             # Análises ad-hoc com dbt
├── macros/               # Macros reutilizáveis do dbt
├── seeds/                # Arquivos CSV para carregamento
├── tests/                # Testes personalizados
├── dbt_project.yml       # Arquivo de configuração do dbt
├── profiles.yml          # Configurações de conexão do dbt
├── .env                  # Arquivo de variáveis de ambiente (não versionado)
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Tecnologias Utilizadas
- **Python**: Linguagem de programação principal
- **Streamlit**: Framework para criação de dashboards interativos
- **Pandas**: Manipulação e análise de dados
- **SQLAlchemy**: ORM para interação com o banco de dados
- **PostgreSQL**: Banco de dados relacional
- **dbt (data build tool)**: Ferramenta para transformação de dados
- **yfinance**: API para obtenção de dados financeiros

## Funcionalidades
- Visualização de preços históricos de commodities
- Conexão direta com banco de dados PostgreSQL
- Interface de usuário intuitiva e responsiva
- Possibilidade de expansão para análises mais complexas

## Configuração do Ambiente

### Pré-requisitos
- Python 3.7+
- PostgreSQL
- dbt Core ou dbt Cloud
- Acesso a um banco de dados com a tabela `public.cb_dm_commodities`

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/jrmesquita7/dbt_classes.git
cd dbt_classes
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:
```
DB_HOST=seu_host
DB_PORT=sua_porta
DB_NAME=seu_nome_de_banco
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_SCHEMA=seu_schema
```

### Execução
Para iniciar o dashboard, execute:
```bash
streamlit run app/app.py
```

## Modelo de Dados
O dashboard utiliza dados da tabela `public.cb_dm_commodities`, que contém informações sobre preços de commodities ao longo do tempo. Esta tabela é gerada através de transformações dbt a partir de dados brutos.

## Desenvolvimento com dbt (data build tool)

### Estrutura de Pastas do dbt
O dbt segue uma estrutura de pastas específica para organizar os modelos de transformação de dados:

- **models/**: Contém todos os modelos SQL que serão compilados e executados pelo dbt
  - **staging/**: Modelos que limpam e padronizam dados brutos (prefixo `stg_`)
  - **intermediate/**: Modelos que combinam e transformam dados de staging (prefixo `int_`)
  - **marts/**: Modelos finais prontos para consumo por usuários de negócios (prefixo `mart_`)
- **macros/**: Funções reutilizáveis escritas em Jinja que podem ser chamadas nos modelos
- **seeds/**: Arquivos CSV estáticos que são carregados no banco de dados
- **snapshots/**: Implementações de SCD (Slowly Changing Dimensions) tipo 2
- **tests/**: Testes personalizados para validar dados
- **analyses/**: Consultas SQL que não geram modelos persistentes

### Configuração do dbt

1. Configure seu arquivo `profiles.yml` (geralmente localizado em `~/.dbt/`):
```yaml
dbt_classes:
  target: dev
  outputs:
    dev:
      type: postgres
      host: [seu_host]
      port: [sua_porta]
      user: [seu_usuario]
      pass: [sua_senha]
      dbname: [seu_banco_de_dados]
      schema: [seu_schema]
      threads: 4
```

2. Verifique a configuração do projeto no arquivo `dbt_project.yml`:
```yaml
name: 'dbt_classes'
version: '1.0.0'
config-version: 2

profile: 'dbt_classes'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
analysis-paths: ["analyses"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  dbt_classes:
    staging:
      +materialized: view
    intermediate:
      +materialized: view
    marts:
      +materialized: table
```

### Comandos Úteis do dbt

#### Comandos Básicos
```bash
# Inicializar um novo projeto dbt
dbt init [nome_do_projeto]

# Executar todos os modelos
dbt run

# Executar um modelo específico
dbt run --select [nome_do_modelo]

# Executar modelos em um diretório específico
dbt run --select staging.*

# Executar modelos e seus dependentes
dbt run --select +[nome_do_modelo]

# Executar modelos e suas dependências
dbt run --select [nome_do_modelo]+
```

#### Testes e Documentação
```bash
# Executar todos os testes
dbt test

# Testar um modelo específico
dbt test --select [nome_do_modelo]

# Gerar documentação
dbt docs generate

# Servir documentação localmente
dbt docs serve
```

#### Gerenciamento de Dependências
```bash
# Instalar pacotes definidos em packages.yml
dbt deps

# Limpar artefatos gerados
dbt clean
```

#### Debugging e Análise
```bash
# Compilar modelos sem executá-los
dbt compile

# Mostrar a linhagem de um modelo
dbt ls --select [nome_do_modelo]

# Mostrar a linhagem detalhada
dbt ls --select [nome_do_modelo] --resource-type model
```

### Documentação do dbt
Para gerar e visualizar a documentação completa do seu projeto dbt:

```bash
# Gerar documentação
dbt docs generate

# Servir documentação em http://localhost:8080
dbt docs serve
```

A documentação inclui:
- Linhagem de dados (DAG)
- Descrições de modelos e colunas
- Testes aplicados
- SQL compilado
- Estatísticas de execução

### Boas Práticas com dbt

1. **Nomenclatura Consistente**:
   - `stg_`: Modelos de staging
   - `int_`: Modelos intermediários
   - `mart_`: Modelos finais

2. **Documentação**:
   - Documente todos os modelos e colunas usando blocos YAML
   - Inclua descrições de negócios claras

3. **Testes**:
   - Aplique testes de integridade (unique, not_null, relationships, accepted_values)
   - Desenvolva testes personalizados para regras de negócio complexas

4. **Modularização**:
   - Use macros para lógica repetitiva
   - Divida modelos complexos em partes menores e reutilizáveis

5. **Materialização Apropriada**:
   - Views para modelos de staging e intermediários
   - Tables para modelos finais de consumo
   - Incremental para tabelas grandes com atualizações frequentes

## Solução de Problemas

### Erro de Conexão com o Banco de Dados
Se você encontrar erros relacionados à conexão com o banco de dados:
- Verifique se o arquivo `.env` está configurado corretamente
- Certifique-se de que as variáveis de ambiente estão sendo carregadas
- Confirme se o banco de dados está acessível a partir do seu ambiente

### Erro na Conversão de Porta
Se você encontrar o erro `ValueError: invalid literal for int() with base 10: 'None'`:
- Verifique se a variável `DB_PORT` está definida no arquivo `.env`
- Certifique-se de que o valor da porta é um número inteiro válido

### Erros Comuns do dbt
- **Compilation Error**: Verifique a sintaxe SQL e Jinja
- **Database Error**: Verifique permissões e conexões
- **Dependency Error**: Verifique se todos os modelos referenciados existem

## Contribuição
Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença
[Especifique a licença do seu projeto aqui]

## Contato
[Seus dados de contato ou do mantenedor do projeto]

---

Este README fornece uma visão geral abrangente do projeto de Dashboard de Commodities, incluindo instruções detalhadas sobre o uso do dbt, sua estrutura de pastas e comandos úteis para desenvolvimento e manutenção do pipeline de dados.
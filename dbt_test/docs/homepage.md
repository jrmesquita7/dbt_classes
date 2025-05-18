{% docs __overview__ %}

# Projeto dbt_classes

## Visão Geral

Este projeto utiliza o dbt (data build tool) para transformação de dados como parte do aprendizado e aplicação prática de conceitos de modelagem de dados. O repositório `dbt_classes` contém modelos, testes e documentação que demonstram as melhores práticas de transformação de dados usando dbt.

## Estrutura do Projeto

O projeto está organizado seguindo as convenções recomendadas pelo dbt:

- **models/**: Transformações SQL organizadas por domínio
- **tests/**: Validações para garantir a qualidade dos dados
- **macros/**: Funções SQL reutilizáveis
- **seeds/**: Dados estáticos em formato CSV
- **docs/**: Documentação do projeto

## Modelos Implementados

### Staging
Modelos que extraem e padronizam dados das fontes originais.

### Intermediate
Transformações intermediárias que preparam os dados para os modelos finais.

### Marts
Modelos finais organizados por área de negócio, prontos para análise.

## Como Utilizar

Para executar todos os modelos:

```bash
dbt run
```

Para executar testes nos modelos:

```bash
dbt test
```

Para gerar e visualizar esta documentação:

```bash
dbt docs generate
dbt docs serve
```

## Fontes de Dados

Este projeto utiliza as seguintes fontes de dados:
- [Liste suas fontes de dados aqui]

## Convenções Adotadas

- Nomes de modelos em snake_case
- Modelos staging com prefixo `stg_`
- Modelos intermediários com prefixo `int_`
- Fatos com prefixo `fct_`
- Dimensões com prefixo `dim_`

## Objetivos de Aprendizado

Este projeto foi desenvolvido como parte do processo de aprendizado de dbt, com foco em:
- Modelagem dimensional
- Testes de dados
- Documentação de código
- Boas práticas de engenharia de dados

## Próximos Passos

- [Liste aqui os próximos desenvolvimentos planejados]

## Recursos Úteis

- [Documentação oficial do dbt](https://docs.getdbt.com/)
- [Guia de estilo do dbt](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md)
- [Discourse do dbt](https://discourse.getdbt.com/)

{% enddocs %}

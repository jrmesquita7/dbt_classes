with commodities_1 as (
    select 
        data,
        simbolo,
        valor_fechamento
    from {{ ref('cb_stg_commodities') }}
),

movimentacao as (
    select
        data as data,
        simbolo as simbolo,
        acao as acao,
        quantidade as quantidade
    from {{ ref('cb_stg_movimentacao_commodities') }}
),

joined as (
    select
        c.*,
        m.acao,
        m.quantidade
    from
        commodities_1 c
    inner join 
        movimentacao m
    on
        c.data = m.data
    and c.simbolo = m.simbolo
),

last_day as (
    select 
        max(data) as max_date
    from 
        joined
),

filtered as (
    select 
        *
    from
        joined
    where 
        data = (select max_date from last_day)
)

-- SELECT FINAL
select * from filtered

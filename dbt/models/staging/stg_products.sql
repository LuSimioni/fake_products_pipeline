with source as (
    select * from {{ source('staging', 'STG_PRODUCTS') }}
)
select
    id              as product_id,
    title           as product_title,
    price,
    category,
    description,
    rating_rate,
    rating_count
from source
with source as (
    select * from {{ source('staging', 'STG_USERS') }}
)
select
    id              as user_id,
    email,
    username,
    firstname,
    lastname,
    firstname || ' ' || lastname as full_name,
    city
from source
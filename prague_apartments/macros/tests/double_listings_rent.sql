{% test double_listings_rent(model, column_name) %}

depends_on: {{ ref('silver_prague_apartments_for_rent') }}

select 
    listing_id,
    count(distinct listing_id)

from {{ ref('silver_prague_apartments_for_rent') }}

group by 1

having count(distinct listing_id) > 1

{% endtest %}
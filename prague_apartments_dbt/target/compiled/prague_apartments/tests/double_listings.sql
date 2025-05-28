

select 
    listing_id,
    count(distinct listing_id)

from "prague_apartments"."main"."silver_prague_apartments_for_rent"

group by 1

having count(distinct listing_id) > 1
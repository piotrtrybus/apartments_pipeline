

depends_on: "d8tltfgi9rccg8"."public"."silver_prague_apartments_for_sale"

select 
    listing_id,
    count(distinct listing_id)

from "d8tltfgi9rccg8"."public"."silver_prague_apartments_for_sale"

group by 1

having count(distinct listing_id) > 1


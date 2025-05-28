

depends_on: "dfrcqf3u6sgd77"."public"."silver_prague_apartments_for_sale"

select 
    listing_id,
    count(distinct listing_id)

from "dfrcqf3u6sgd77"."public"."silver_prague_apartments_for_sale"

group by 1

having count(distinct listing_id) > 1


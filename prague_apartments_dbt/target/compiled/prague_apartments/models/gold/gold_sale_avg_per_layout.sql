select
    property_layout,
    cast(round(avg(price_czk)::numeric,0) as float) avg_price_czk,
    cast(round(avg(area_m2)::numeric,1) as float) avg_area_m2

from "dfrcqf3u6sgd77"."public"."silver_prague_apartments_for_sale"

group by 1

having count(distinct listing_id) >= 2

order by 2 desc
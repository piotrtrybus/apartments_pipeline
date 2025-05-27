select
    property_district,
    cast(round(avg(price_czk)::numeric,0) as float) avg_rent_czk,
    cast(round(avg(area_m2)::numeric,0) as float) avg_area_m2,
    cast(round(avg(rooms_without_kitchen)::numeric,1) as float) avg_rooms_without_kitchen

from {{ref('silver_prague_apartments_for_rent')}}

group by 1

having count(distinct listing_id) >= 2

order by 2 desc
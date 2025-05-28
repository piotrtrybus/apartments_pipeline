
  
    

  create  table "d8tltfgi9rccg8"."public"."gold_sale_avg_per_district__dbt_tmp"
  
  
    as
  
  (
    select
    property_district,
    cast(round(avg(price_czk)::numeric,0) as float) avg_price_czk,
    cast(round(avg(area_m2)::numeric,0) as float) avg_area_m2,
    cast(round(avg(rooms_without_kitchen)::numeric,1) as float) avg_rooms_without_kitchen

from "d8tltfgi9rccg8"."public"."silver_prague_apartments_for_sale"

group by 1

having count(distinct listing_id) >= 2

order by 2 desc
  );
  
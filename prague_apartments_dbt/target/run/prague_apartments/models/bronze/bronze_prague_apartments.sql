
  
  create view "prague_apartments"."main"."bronze_prague_apartments__dbt_tmp" as (
    with numbered_listings as(
    select 
    eventid as listing_id,
    title as property_title,
    district as property_district,
    property_type as listing_type,
    price_czk,
    layout as property_layout,
    area_m2,
    timestamp,
    cast(timestamp as date) as date,
    row_number() over (partition by listing_id order by timestamp desc) as row_number

from prague_apartments
)

select * from numbered_listings
where row_number = 1
  );

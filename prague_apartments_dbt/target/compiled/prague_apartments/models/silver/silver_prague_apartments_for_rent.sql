with __dbt__cte__bronze_prague_apartments as (
with numbered_listings as(
    select 
    eventid as listing_id,
    title as property_title,
    district as property_district,
    property_type as listing_type,
    regexp_replace(price_czk, '[^0-9]', '', 'g')::BIGINT as price_czk,
    layout as property_layout,
    area_m2,
    case when layout like '%kk%' or layout like '%+1%' then False else True end as atypical_listing,
    timestamp,
    cast(timestamp as date) as date,
    row_number() over (partition by eventid order by timestamp desc) as row_number

from prague_apartments
)

select * from numbered_listings
where row_number = 1
) select
    cast(listing_id as varchar) listing_id,
    cast(property_title as varchar) property_title,
    cast(property_district as varchar) property_district,
    cast(price_czk as bigint) price_czk,
    cast(property_layout as varchar) property_layout,
    cast(
        
        case 
            when property_layout = '1+kk' then 1
            when property_layout = '2+kk' then 2
            when property_layout = '3+kk' then 3
            when property_layout = '4+kk' then 4
            when property_layout = '5+kk' then 5
            when property_layout = '6+kk' then 6
            when property_layout = '7+kk' then 7
            when property_layout = '1+1' then 1
            when property_layout = '2+1' then 2
            when property_layout = '3+1' then 3
            when property_layout = '4+1' then 4
            when property_layout = '5+1' then 5
            when property_layout = '6+1' then 6
            when property_layout = '7+1' then 7
        end as float

    ) as rooms_without_kitchen,
    cast(area_m2 as bigint) area_m2,
    cast(date as date) date

from __dbt__cte__bronze_prague_apartments

where 
    listing_type = 'For Rent'
    and
    atypical_listing = False
    and
    price_czk != 0
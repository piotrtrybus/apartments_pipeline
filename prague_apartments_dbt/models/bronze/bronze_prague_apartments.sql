with numbered_listings as(
    select 
    eventid as listing_id,
    title as property_title,
    link as listing_link,
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
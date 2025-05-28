select
    cast(listing_id as varchar) listing_id,
    cast(property_title as varchar) property_title,
    cast(listing_link as varchar) listing_link,
    cast(property_district as varchar) property_district,
    cast(price_czk as bigint) price_czk,
    cast(property_layout as varchar) property_layout,
    cast(left(property_layout,1) as bigint) rooms_without_kitchen,
    cast(area_m2 as bigint) area_m2,
    cast(date as date) date

from {{ref('bronze_prague_apartments')}}

where 
    listing_type = 'For Rent'
    and
    atypical_listing = False
    and
    price_czk != 0
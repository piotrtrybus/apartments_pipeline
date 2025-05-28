select
    cast(listing_id as varchar) listing_id,
    cast(property_title as varchar) property_title,
    cast(listing_link as varchar) listing_link,
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

from {{ref('bronze_prague_apartments')}}

where 
    listing_type = 'For Sale'
    and
    atypical_listing = False
    and
    price_czk != 0
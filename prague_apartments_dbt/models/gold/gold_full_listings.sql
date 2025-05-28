select
    listing_id,
    property_title,
    listing_link,
    property_district,
    price_czk,
    property_layout,
    area_m2,
    'Rental' as listing_type
from {{ ref('silver_prague_apartments_for_rent') }}

union all

select
    listing_id,
    property_title,
    listing_link,
    property_district,
    price_czk,
    property_layout,
    area_m2,
    'Sale' as listing_type
from {{ ref('silver_prague_apartments_for_sale') }}

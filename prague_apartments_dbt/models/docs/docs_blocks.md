{% docs listing_id %}
Unique ID (SHA-256 hash) of a listing based on property title, location and property type.
{% enddocs %}

{% docs property_title %}
Title of the property containing basic information from the listing.
{% enddocs %}

{% docs property_district %}
The district of Prague in which the property is located
{% enddocs %}

{% docs listing_type %}
Type of listings: Rental or Sale
{% enddocs %}

{% docs listing_link %}
Link to the listing on sreality.cz.
{% enddocs %}

{% docs price_czk %}
Price of the property: monthly rent or purchase price in Czech Crowns.
{% enddocs %}

{% docs property_layout %}
Layout of the property. Bathroom not counted.
{% enddocs %}

{% docs area_m2 %}
Full area of the property in meters squared.
{% enddocs %}

{% docs timestamp %}
Timestamp of when the property was scraped. Not a timestamp of the listing being uploaded.
{% enddocs %}

{% docs date %}
Date extracted from the timestamp. 
{% enddocs %}

{% docs rooms_without_kitchen %}
Number of rooms without kitchen in the property. Example: 2kk and 2+1 both counted as 2.
{% enddocs %}

{% docs avg_price_czk %}
Mean monthly rent shown in Czech Crowns.
{% enddocs %}

{% docs avg_area_m2 %}
Mean area of the property in square meters.
{% enddocs %}

{% docs avg_rooms_without_kitchen %}
Mean number of rooms excluding kitchen as a separate room. Based on rooms_without_kitchen.
{% enddocs %}
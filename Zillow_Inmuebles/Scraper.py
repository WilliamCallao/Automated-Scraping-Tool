from homeharvest import scrape_property
from datetime import datetime

current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"RawData_{current_timestamp}.csv"

location = "San Diego, CA"  # ubicación
listing_type = "for_sale"  # "for_sale", "for_rent", "sold"
past_days = 30000

properties = scrape_property(
    location=location,
    listing_type=listing_type,
    past_days=past_days,
)

print(f"Number of properties: {len(properties)}")
properties.to_csv(filename, index=False)
print(properties.head())

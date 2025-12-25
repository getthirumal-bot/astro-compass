# Quick test - paste this code to see country language mapping

from country_utils import detect_country_from_phone

print("Country → Languages Mapping:")
print("=" * 60)

countries_to_test = [
    ('India', '+91'),
    ('Nigeria', '+234'),
    ('Ghana', '+233'),
    ('UAE', '+971'),
    ('Singapore', '+65'),
    ('USA', '+1'),
]

for name, code in countries_to_test:
    info = detect_country_from_phone(code + "1234567890")
    if info:
        print(f"\n{name} ({code}):")
        print(f"  → {', '.join(info['languages'])}")

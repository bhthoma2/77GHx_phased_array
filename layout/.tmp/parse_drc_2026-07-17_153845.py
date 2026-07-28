import xml.etree.ElementTree as ET
from collections import Counter

tree = ET.parse('/home/bthomas3/Videos/77GHz_phased_array/layout/drc_top.lyrdb')
root = tree.getroot()

counts = Counter()
for cat in root.iter('category'):
    name_el = cat.find('name')
    items = cat.find('items')
    if name_el is not None and items is not None:
        n = len(list(items.iter('item')))
        if n > 0:
            counts[name_el.text] = n

print(f"Total DRC violations: {sum(counts.values())}")
print(f"Categories with violations: {len(counts)}")
print()
for rule, cnt in counts.most_common(30):
    print(f"  {rule:30s} {cnt:5d}")

"""Strip Python 3.9+ type annotations from cni module for Python 3.6 compat."""
import re
import os
import glob

CNI_DIR = "/home/bthomas3/Videos/IHP-Open-PDK/ihp-sg13g2/libs.tech/klayout/python/pycell4klayout-api/source/python/cni"

for pyfile in glob.glob(os.path.join(CNI_DIR, "*.py")):
    with open(pyfile, 'r') as f:
        content = f.read()

    orig = content

    # Remove return type annotations: ) -> Type:  =>  ):
    content = re.sub(r'\)\s*->\s*[^:]+:', '):', content)

    # Remove parameter type annotations: param: Type  =>  param
    # But be careful not to remove default values
    # Match: word: Type (not followed by =)  or  word: Type = default
    # Replace param: list[X] with just param
    content = re.sub(r'(\w+)\s*:\s*(?:list|dict|tuple|set|frozenset|Optional|Union|List|Dict|Tuple|Set)\[[^\]]*\]', r'\1', content)
    # Simple type annotations: param: Type (where Type is a single word)
    content = re.sub(r'(\w+)\s*:\s*(?:str|int|float|bool|None|Box|Point|Layer|Shape|Pin|Net|Term|Rect|Path|PhysicalComponent|Grouping|ShapeFilter|Instance|DloGen|PointList|Transform|Orientation|Location)\b(?!\s*=)', r'\1', content)

    if content != orig:
        with open(pyfile, 'w') as f:
            f.write(content)
        print(f"Patched: {os.path.basename(pyfile)}")

print("Done")

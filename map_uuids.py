import os
import re

def get_uuid_from_node(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            match = re.search(r'^uuid=(.*)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return None

def get_uuid_from_filename(filename):
    # Name.Type.UUID.Extension
    parts = filename.split('.')
    if len(parts) >= 4:
        # The UUID is the part(s) before the last dot (extension)
        # But wait, Stroom format is Name.Type.UUID.Extension
        # If there are dots in the UUID, it becomes complicated.
        # Let's assume the first two parts are Name and Type, and the last is Extension.
        # Everything in between is UUID.
        uuid_parts = parts[2:-1]
        return ".".join(uuid_parts)
    return None

def scan_content(base_path):
    uuid_map = {}
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if f.endswith('.node') or f.endswith('.meta'):
                ext = f.split('.')[-1]
                uuid = get_uuid_from_filename(f)
                if uuid:
                    if uuid not in uuid_map:
                        uuid_map[uuid] = []
                    uuid_map[uuid].append(os.path.join(root, f))
                
                if f.endswith('.node'):
                    internal_uuid = get_uuid_from_node(os.path.join(root, f))
                    if internal_uuid and internal_uuid != uuid:
                        print(f"MISMATCH: Internal UUID '{internal_uuid}' vs Filename UUID '{uuid}' in {f}")

    return uuid_map

base_path = "source/generated_rules_demo/stroomContent"
uuid_map = scan_content(base_path)

print("\n--- Missing Files Report ---")
for uuid, paths in uuid_map.items():
    extensions = [p.split('.')[-1] for p in paths]
    if 'node' in extensions and 'meta' not in extensions:
        # Ignore folders
        is_folder = any('.Folder.' in p for p in paths)
        if not is_folder:
            print(f"UUID {uuid} has .node but NO .meta:")
            for p in paths: print(f"  {p}")
    elif 'meta' in extensions and 'node' not in extensions:
        print(f"UUID {uuid} has .meta but NO .node:")
        for p in paths: print(f"  {p}")

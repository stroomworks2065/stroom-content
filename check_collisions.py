import os
import re

def get_type_from_filename(filename):
    parts = filename.split('.')
    if len(parts) >= 4:
        return parts[1]
    return None

def get_uuid_from_filename(filename):
    parts = filename.split('.')
    if len(parts) >= 4:
        # Everything between type and extension
        return ".".join(parts[2:-1])
    return None

def scan_content(base_path):
    uuid_type_map = {}
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if f.endswith('.node') or f.endswith('.meta'):
                uuid = get_uuid_from_filename(f)
                obj_type = get_type_from_filename(f)
                if uuid and obj_type:
                    if uuid not in uuid_type_map:
                        uuid_type_map[uuid] = {}
                    if obj_type not in uuid_type_map[uuid]:
                        uuid_type_map[uuid][obj_type] = set()
                    uuid_type_map[uuid][obj_type].add(os.path.join(root, f))
    return uuid_type_map

base_path = "source/generated_rules_demo/stroomContent"
uuid_type_map = scan_content(base_path)

print("\n--- UUID Collision Report (Multiple Types for same UUID) ---")
for uuid, types in uuid_type_map.items():
    if len(types) > 1:
        # Ignore cases where one is 'Folder' (though that shouldn't happen with UUIDs)
        if 'Folder' in types and len(types) == 2:
            continue
        print(f"UUID {uuid} is used by multiple types: {list(types.keys())}")
        for t, paths in types.items():
            print(f"  Type {t}:")
            for p in paths: print(f"    {p}")

print("\n--- Completeness Report (Missing .node or .meta for a Type) ---")
for uuid, types in uuid_type_map.items():
    for obj_type, paths in types.items():
        if obj_type == 'Folder': continue
        exts = {p.split('.')[-1] for p in paths}
        if 'node' not in exts:
            print(f"UUID {uuid} (Type {obj_type}) is missing .node")
        if 'meta' not in exts:
            print(f"UUID {uuid} (Type {obj_type}) is missing .meta")

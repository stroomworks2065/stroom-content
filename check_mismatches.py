import os

def check_dir(dir_path):
    files = os.listdir(dir_path)
    nodes = {f[:-5] for f in files if f.endswith('.node')}
    metas = {f[:-5] for f in files if f.endswith('.meta')}
    
    only_nodes = nodes - metas
    only_metas = metas - nodes
    
    if only_nodes:
        print(f"Only .node in {dir_path}:")
        for f in only_nodes:
            print(f"  {f}.node")
    if only_metas:
        print(f"Only .meta in {dir_path}:")
        for f in only_metas:
            print(f"  {f}.meta")

base_path = "source/generated_rules_demo/stroomContent/Generated_Rules_Demo.Folder.28860f43-0f82-4b0c-952a-d46d1017c75f"
datagen_path = os.path.join(base_path, "Data_Generators.Folder.7b1ff852-7f37-46e3-b9f7-777e62f003cc/Windows.Folder.16a4699e-ff6c-47be-aa18-ff6dd47d8206")
rules_path = os.path.join(base_path, "Rules.Folder.5151618f-2bdb-4525-8c7a-608950243d77/Windows.Folder.fea4f9f2-ebe0-424c-920d-bc292fcf7142")

print("Checking Data Generators...")
check_dir(datagen_path)

print("\nChecking Rules...")
for sub in ["experimental", "stable", "test"]:
    p = os.path.join(rules_path, f"{sub}.Folder." + ("c339b091-9377-480c-b91a-c7e9e8336157" if sub == "experimental" else "ae10b082-5c04-41e9-ad08-62e97e60c9bb" if sub == "stable" else "ca66a834-d491-471d-856d-9abd78faacc2"))
    if os.path.exists(p):
        check_dir(p)

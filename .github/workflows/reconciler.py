import json
from pathlib import Path

ROOT = Path(__file__).parent
MANIFEST = ROOT/"manifest.json"

def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def reconcile(shards):
    seen = {}
    for shard in shards:
        path = ROOT/shard["file"]
        rows = load_jsonl(path)
        for obj in rows:
            seen[obj["id"]] = obj  # última versão substitui
        # sobrescreve shard sem duplicatas internas
        write_jsonl(path, list({o["id"]:o for o in rows}.values()))
    return list(seen.values())

def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    all_objs = reconcile(manifest["shards"])
    print("Reconciliação concluída ✅")
    print("Objetos únicos:", len(all_objs))

if __name__ == "__main__":
    main()

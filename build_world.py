import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
MANIFEST = ROOT/"manifest.json"
OUTPUT = ROOT/"world_master.json"

def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    world = {
        "version": manifest.get("version", 1),
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "characters": [], "locations": [], "items": [], "events": []
    }
    for shard in manifest["shards"]:
        path = ROOT/shard["file"]
        rows = list(load_jsonl(path))
        world[shard["type"]].extend(rows)

    OUTPUT.write_text(json.dumps(world, indent=2, ensure_ascii=False), encoding="utf-8")
    print("world_master.json gerado com sucesso ✅")

if __name__ == "__main__":
    main()

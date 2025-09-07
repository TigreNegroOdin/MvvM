import json, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
MANIFEST = ROOT/"manifest.json"

def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows

def main():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids = set()
    characters = {}
    locations = {}
    problems = []

    for shard in manifest["shards"]:
        p = ROOT/shard["file"]
        if not p.exists():
            problems.append(f"Shard não encontrado: {p}")
            continue
        rows = load_jsonl(p)
        t = shard["type"]
        for obj in rows:
            if "id" not in obj:
                problems.append(f"{shard['file']}: objeto sem 'id'")
                continue
            if obj["id"] in ids:
                problems.append(f"ID duplicado: {obj['id']}")
            ids.add(obj["id"])

            if t == "characters":
                characters[obj["id"]] = obj
            elif t == "locations":
                locations[obj["id"]] = obj
            elif t == "events":
                try:
                    datetime.fromisoformat(obj["when"].replace("Z","+00:00"))
                except Exception:
                    problems.append(f"Evento {obj.get('id')} 'when' inválido: {obj.get('when')}")
                if obj.get("where") and obj["where"] not in locations:
                    problems.append(f"Evento {obj['id']} referencia local inexistente: {obj['where']}")
                for a in obj.get("actors", []):
                    if a not in characters:
                        problems.append(f"Evento {obj['id']} referencia personagem inexistente: {a}")

    if problems:
        print("\n=== PROBLEMAS ENCONTRADOS ===")
        for p in problems:
            print("-", p)
        sys.exit(1)
    else:
        print("Validação OK ✅")

if __name__ == "__main__":
    main()

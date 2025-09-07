import json

def main():
    with open("World.json", "r", encoding="utf-8") as f:
        world = json.load(f)
    print("=== Mundo Vivo carregado ===")
    print(json.dumps(world, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

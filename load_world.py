import os
import zipfile

# URL do repositório
REPO_URL = "https://github.com/TigreNegroOdin/MvvM"
LOCAL_PATH = "repositorio_mundo"

# Clona ou atualiza o repositório
if not os.path.exists(LOCAL_PATH):
    os.system(f"git clone {REPO_URL} {LOCAL_PATH}")
else:
    os.system(f"cd {LOCAL_PATH} && git pull")

# Função pra ler arquivos de texto
def ler_arquivo(caminho):
    try:
        with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return ""

# Carrega todos os arquivos do repositório
base_mundo = {}

for root, _, files in os.walk(LOCAL_PATH):
    for file in files:
        caminho = os.path.join(root, file)

        if file.endswith((".txt", ".md", ".py")):
            base_mundo[file] = ler_arquivo(caminho)

        elif file.endswith(".zip"):
            with zipfile.ZipFile(caminho, "r") as zip_ref:
                for nome in zip_ref.namelist():
                    if nome.endswith((".txt", ".md")):
                        conteudo = zip_ref.read(nome).decode("utf-8", errors="ignore")
                        base_mundo[f"{file}:{nome}"] = conteudo

print("Arquivos carregados do mundo:")
for k in base_mundo.keys():
    print("-", k)

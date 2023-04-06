with open("env.eniac", "r") as f:
    data = f.readlines()

nome = None
idade = None

for line in data:
    if "nome" in line:
        nome = line.split("=")[1].strip()
    elif "idade" in line:
        idade = line.split("=")[1].strip()

print(f"A pessoa tem {idade} anos e se chama {nome}")
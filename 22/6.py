from pathlib import Path

with open(Path(__file__).parent/"6.txt") as f:
    text = f.read()

for pos in range(13, len(text)):
    subtext = text[pos-13:pos+1]
    print(subtext)
    if len(set(subtext)) == 14:
        print(pos+1)
        break

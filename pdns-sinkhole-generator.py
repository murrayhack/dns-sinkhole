import sys
import requests
import toml
from pathlib import Path
from typing import List

def luaify(input: List[str]) -> str:
    input.sort()
    input = list(dict.fromkeys(input))  # Deduplicate
    output = "return{\n"
    for entry in input:
        output += f"    \"{entry}\",\n"
    output = output.rstrip(',\n') + "\n}"
    return output

def process(tgt: List[str], path: Path) -> None:
    urls = []
    for url in tgt:
        try:
            response = requests.get(url)
            response.raise_for_status()
            body = response.text
        except requests.RequestException as e:
            print(f"Got busted URL: {url} with error {e}")
            continue

        for line in body.splitlines():
            if not line or line.startswith('#'):
                continue
            line = line.split('#')[0].strip()
            urls.append(line.strip())

    output = luaify(urls)
    with path.open('w') as o:
        o.write(output)

def main(config_path: Path) -> None:
    with config_path.open('r') as cf:
        cfg = cf.read()
    
    config = toml.loads(cfg)

    process(config['blocklists'], Path(config['blocklist_output']))
    process(config['permitted'], Path(config['permitted_output']))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdns-sinkhole-generator.py <config_path>")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    main(config_path)

import sys
import requests
import yaml
from pathlib import Path
from typing import List

def convert_to_lua_table(url_list: List[str]) -> str:
    url_list.sort()
    url_list = list(dict.fromkeys(url_list))  # Deduplicate
    lua_table = "return{\n"
    for url in url_list:
        lua_table += f"    \"{url}\",\n"
    lua_table = lua_table.rstrip(',\n') + "\n}"
    return lua_table

def process_urls(urls_to_process: List[str], output_file_path: Path) -> None:
    cleaned_urls = []
    for url in urls_to_process:
        try:
            response = requests.get(url)
            response.raise_for_status()
            response_body = response.text
        except requests.RequestException as e:
            print(f"Failed to fetch URL: {url} with error {e}")
            continue

        for line in response_body.splitlines():
            if not line or line.startswith('#'):
                continue
            line = line.split('#')[0].strip()
            cleaned_urls.append(line.strip())

    lua_formatted_output = convert_to_lua_table(cleaned_urls)
    with output_file_path.open('w') as output_file:
        output_file.write(lua_formatted_output)

def main(configuration_file_path: Path) -> None:
    with configuration_file_path.open('r') as config_file:
        configuration = yaml.safe_load(config_file)

    process_urls(configuration['blocklists'], Path(configuration['blocklist_output']))
    process_urls(configuration['permitted'], Path(configuration['permitted_output']))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <config_path>")
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    main(config_path)

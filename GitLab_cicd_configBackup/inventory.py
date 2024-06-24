import yaml
import sys
from pathlib import Path

def loadInventory(inventoryFile):
    f = open(inventoryFile)
    inv = yaml.safe_load(f)

    return inv

def main():
    """

    """

    inventory = loadInventory('inventory.yaml')

    for entry in inventory['hosts']:

        # Checking the local filesystem and create a folder for each
        # NE if it does not yet exist

        print("Creating sub-directory for each host if needed\n")
        filepath = Path(entry+'/config.json')
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if filepath.is_file():
            print("File exist")
        else:
            print("File not exist")
            with filepath.open("w", encoding ="utf-8") as f:
                f.write('# Empty config.json file automatically created through pipeline')
                f.close()


if __name__ == "__main__":
    main()

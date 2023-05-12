import json
import csv
import os
from typing import List, Dict, Any
from pathlib import Path
import shutil


root = Path(".")
prices_csv = root / "prices_2023_04_23.csv"
results_dir = root / "results"
# results_json = root / "results_2023_04_23.json"

def read_csv(file_path: Path) -> List[Dict[str, str]]:
    with open(file_path, "r") as f:
        csv_reader = csv.DictReader(f, delimiter="|")
        return list(csv_reader)


def write_to_file(data: Dict[str, Any], file_path: Path):
    with open(file_path, "w") as f:
        f.write(json.dumps(data))


def underscore(word: str) -> str:
    return (
        word.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(",", "_")
        .replace("-", "_")
        .replace("&", "_and_")
        .replace("(", "_")
        .replace(")", "_")
        .replace("__", "_")
        .replace("__", "_")
        .replace("__", "_")
        .replace("__", "_")
        .strip("_")
    )


def main():
    shutil.rmtree(results_dir, ignore_errors=True)
    results_dir.mkdir()

    rows = read_csv(
        prices_csv
    )
    rows_by_name = get_rows_by_name(rows)
    # write_to_file(rows_by_name, results_json)
    for contract_name, contract in rows_by_name.items():

        contract_folder = results_dir / underscore(contract_name)
        contract_folder.mkdir(exist_ok=True)
        for product_name, products in contract.items():
            results_json = contract_folder / f"{underscore(product_name)}.json"
            write_to_file(products, results_json)
    # rows_by_name = [row["Contract_Name"] for row in rows]
    print("")


def get_rows_by_name(rows: List[Dict[str,str]]) -> Dict[str, Dict[str, Dict[str,str]]]:
    rows_by_name = {}
    for row in rows:
        contract_name = row["Contract_Name"]
        product_name = row["Product_Name"]
        if contract_name not in rows_by_name.keys():
            rows_by_name[contract_name] = {}
        if product_name not in rows_by_name[contract_name].keys():
            rows_by_name[contract_name][product_name] = []
        no_name = row.copy()
        del no_name["Contract_Name"]
        del no_name["Product_Name"]
        rows_by_name[contract_name][product_name].append(no_name)
    return rows_by_name


if __name__ == "__main__":
    main()

from wikitable import *
import os

classes = [
"Amazon",
"Assassin",
"Barbarian",
"Druid",
"Necromancer",
"Paladin",
"Sorceress",
]

for class_name in classes:
    raw_html = get_html(f'https://projectdiablo2.miraheze.org/wiki/All_{class_name}_Skills')
    tables = get_tables(raw_html)
    os.makedirs(class_name, exist_ok=True)
    to_csv(tables, f'{class_name}/')

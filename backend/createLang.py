import os
import json

# Ask user for input
language = input("Enter the language name: ").strip()
language_key = input("Enter the language short key (ex: ta, en, etc.): ").strip()

# Paths
base_dir = os.path.dirname(__file__)
keyfile_path = os.path.join(base_dir, "keys.json")
translations_folder = os.path.join(base_dir, "translations")

file_path = os.path.join(translations_folder, f"{language}.json")

# Load keys
with open(keyfile_path, "r", encoding="utf-8") as f:
    translations_data = json.load(f)

# Prepare all translations in a list or dict
all_translations = []
for key in translations_data:
    entry = {
        "key": translations_data[key],
        "lang": language_key,
        "name": language,
        "value": ""
    }
    all_translations.append(entry)

# Write once after the loop
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(all_translations, f, ensure_ascii=False, indent=4)

print(f"✅ Created translation file: {file_path}")
print(f"Total keys added: {len(all_translations)}")

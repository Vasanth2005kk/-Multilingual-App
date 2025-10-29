import os
import json
from app import app, Translation, db

def create_language():
    """Create new language file and insert into database"""
    language = input("Enter the language name: ").strip()
    language_key = input("Enter the language short key (ex: ta, en, etc.): ").strip()

    base_dir = os.path.dirname(__file__)
    keyfile_path = os.path.join(base_dir, "keys.json")
    translations_folder = os.path.join(base_dir, "translations")
    os.makedirs(translations_folder, exist_ok=True)
    file_path = os.path.join(translations_folder, f"{language}.json")

    # --- Load base translation keys ---
    with open(keyfile_path, "r", encoding="utf-8") as f:
        keys_data = json.load(f)

    # --- Prepare translation entries ---
    all_translations = [
        {
            "key": k,
            "lang": language_key,
            "name": language,
            "value": ""
        }
        for k in keys_data.values()
    ]

    # --- Write JSON file ---
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(all_translations, f, ensure_ascii=False, indent=4)

    print(f"✅ Created translation file: {file_path}")
    print(f"Total keys added: {len(all_translations)}")

    # --- Load into DB ---
    with app.app_context():
        existing_keys = {
            t.key for t in Translation.query.filter_by(lang=language_key).all()
        }

        new_translations = [
            Translation(
                key=item["key"],
                lang=item["lang"],
                name=item["name"],
                value=item["value"]
            )
            for item in all_translations
            if item["key"] not in existing_keys
        ]

        if new_translations:
            db.session.add_all(new_translations)
            db.session.commit()
            print(f"✅ {language} language loaded successfully with {len(new_translations)} new keys.")
        else:
            print(f"⚠️ No new keys added — all translations already exist.")

def delete_language():
    """Delete all translations for a given language key"""
    language_key = input("Enter the language short key to delete (ex: ta, en, etc.): ").strip()
    confirm = input(f"⚠️ Are you sure you want to delete all translations for '{language_key}'? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("❌ Deletion cancelled.")
        return

    with app.app_context():
        count = Translation.query.filter_by(lang=language_key).delete()
        db.session.commit()

        if count > 0:
            print(f"✅ Deleted {count} translation entries for language key '{language_key}'.")
        else:
            print(f"⚠️ No translations found for language key '{language_key}'.")

def main():
    print("Select an option:")
    print("1️⃣  Add / Create a new language")
    print("2️⃣  Delete an existing language")
    choice = input("Enter 1 or 2: ").strip()

    try:
        if choice == "1":
            create_language()
        elif choice == "2":
            delete_language()
        else:
            print("❌ Invalid choice. Please run the script again and select 1 or 2.")
    except FileNotFoundError:
        print("❌ keys.json not found! Please make sure it exists in the same directory.")
    except Exception as e:
        with app.app_context():
            db.session.rollback()
        print(f"❌ Error: {e}") 

if __name__ == "__main__":
    main()

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import json 

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Translation Model
class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), nullable=False)
    lang = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Text, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('key', 'lang', name='unique_key_lang'),)

def init_db():
    with app.app_context():
        db.create_all()

        # Only load defaults if DB is empty
        if Translation.query.first() is None:
            json_path = os.path.join(os.path.dirname(__file__), "translations.json")
            
            with open(json_path, "r", encoding="utf-8") as f:
                translations_data = json.load(f)

            # Convert JSON data into Translation objects
            translations = [
                Translation(
                    key=item["key"],
                    lang=item["lang"],
                    name=item["name"],
                    value=item["value"]
                )
                for item in translations_data
            ]

            db.session.add_all(translations)
            db.session.commit()
            print(f"✅ Database initialized with {len(translations)} translations!")
        else:
            print("ℹ️ Translations already exist in the database.")


# API Endpoint: Get translations by language
@app.route('/api/translations/<lang>', methods=['GET'])
def get_translations(lang):
    try:
        translations = Translation.query.filter_by(lang=lang).all()

        if not translations:
            return jsonify({'error': 'Language not found'}), 404
        
        result = {}
        for trans in translations:

            # Build nested structure (e.g., navbar.home → navbar: {home: "Home"})
            parts = trans.key.split('.')

            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = trans.value
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK'}), 200

# List available languages
@app.route('/api/languages', methods=['GET'])
def get_languages():
    try:
        langs_names = db.session.query(Translation.lang,Translation.name).distinct().all()

        result = []
        for lang,name in langs_names:   
            result.append({'code' : lang , "name" : name})
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# List of datas
@app.route('/api/datas', methods=['GET'])
def get_datas():
    try:
        # Fetch all translations
        translation_rows = Translation.query.all()

        translations = {}
        key_counter = 1  # numeric key counter

        # Temporary dictionary to group translations
        grouped = {}

        # Group translations by their key
        for row in translation_rows:
            if row.key not in grouped:
                grouped[row.key] = {}
            grouped[row.key][row.lang] = row.value

        # Assign numeric keys (1, 2, 3, …)
        for _, lang_dict in grouped.items():
            translations[str(key_counter)] = lang_dict
            key_counter += 1

        return jsonify(translations), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
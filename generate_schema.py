import json
from models import Supplier

def generate_schema():
    schema = Supplier.model_json_schema()
    with open('supplier_schema.json', 'w') as f:
        json.dump(schema, f, indent=2)
    print("Schema generated and saved to supplier_schema.json")

if __name__ == "__main__":
    generate_schema()

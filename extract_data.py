import re
import json
from collections import defaultdict

def extract_insert_statements(sql_file):
    """Extract INSERT statements from SQL dump"""
    with open(sql_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all INSERT statements
    insert_pattern = r"INSERT INTO `(\w+)` VALUES (.+?);"
    matches = re.findall(insert_pattern, content, re.DOTALL)
    
    data = defaultdict(list)
    
    for table_name, values_part in matches:
        # Parse the VALUES part
        # This regex finds each row: (value1, value2, ...)
        row_pattern = r"\(([^)]+)\)"
        rows = re.findall(row_pattern, values_part)
        
        for row in rows:
            # Split values and clean them
            values = [v.strip().strip("'\"") for v in row.split(',')]
            data[table_name].append(values)
    
    return data

def create_django_fixtures(data):
    """Convert extracted data to Django fixture format"""
    fixtures = []
    pk_counter = 1
    
    # Handle web_farsl data
    if 'web_farsl' in data:
        for row in data['web_farsl']:
            fixture = {
                "model": "web.webfarsl",
                "pk": int(row[0]),  # fID
                "fields": {
                    "fname": row[1] if len(row) > 1 else None
                }
            }
            fixtures.append(fixture)
    
    # Handle web_mcust data
    if 'web_mcust' in data:
        for row in data['web_mcust']:
            fixture = {
                "model": "web.webmcust",
                "pk": int(row[0]),  # fID
                "fields": {
                    "fname": row[1] if len(row) > 1 else None,
                    "fpassword": row[2] if len(row) > 2 else None
                }
            }
            fixtures.append(fixture)
    
    # Handle web_pcust data
    if 'web_pcust' in data:
        for row in data['web_pcust']:
            fields = {
                "fcust": int(row[1]) if row[1] and row[1] != 'NULL' else None,
                "fsl": int(row[2]) if row[2] and row[2] != 'NULL' else None,
                "fdoc": row[3] if len(row) > 3 and row[3] != 'NULL' else None,
                "fsdate": row[4] if len(row) > 4 and row[4] != 'NULL' else None,
                "frem": row[5] if len(row) > 5 and row[5] != 'NULL' else None,
                "fsdr": row[6] if len(row) > 6 and row[6] != 'NULL' else None,
                "fscr": row[7] if len(row) > 7 and row[7] != 'NULL' else None,
                "fsbal": row[8] if len(row) > 8 and row[8] != 'NULL' else None,
            }
            
            fixture = {
                "model": "web.webpcust",
                "pk": int(row[0]),  # fAUTO
                "fields": fields
            }
            fixtures.append(fixture)
    
    return fixtures

if __name__ == "__main__":
    print("Extracting data from backup.sql...")
    data = extract_insert_statements('backup.sql')
    
    print(f"Found tables: {list(data.keys())}")
    for table, rows in data.items():
        print(f"  {table}: {len(rows)} rows")
    
    print("Converting to Django fixtures...")
    fixtures = create_django_fixtures(data)
    
    with open('web_data_fixtures.json', 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
    
    print(f"Created web_data_fixtures.json with {len(fixtures)} objects")

# Install required packages
!pip install pandas tqdm --quiet

import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from IPython.display import display, FileLink

# Get JSON file path from user
filename = input("Enter your JSON filename (with extension): ").strip()
file_path = Path(filename)

# Check if the file exists
if not file_path.exists():
    print("File not found. Please check the path and filename.")
else:
    # Create output directories
    split_dir = Path(f"{file_path.stem}_chunks")
    csv_dir = Path(f"{file_path.stem}_csvs")
    split_dir.mkdir(exist_ok=True)
    csv_dir.mkdir(exist_ok=True)

    # Set chunk size
    chunk_size = 10000
    chunk = []
    file_count = 0
    colnames = set()

    print("Scanning JSON file to determine column names (this may take a moment)...")
    with open(file_path, 'r', encoding='utf-8') as f:
        for _, line in zip(range(5000), f):  # Scan first 5000 lines
            try:
                item = json.loads(line)
                colnames.update(item.keys())
            except:
                continue
    colnames = sorted(list(colnames))

    print(f"Total {len(colnames)} columns detected.")

    print("Splitting JSON into chunks with null padding for malformed records...")
    with open(file_path, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(tqdm(f, desc="Splitting", unit="rows"), 1):
            try:
                item = json.loads(line)
            except:
                item = {col: None for col in colnames}
            final_row = {col: item.get(col, None) for col in colnames}
            chunk.append(final_row)

            if idx % chunk_size == 0:
                out_file = split_dir / f"chunk_{file_count}.json"
                with open(out_file, 'w', encoding='utf-8') as out:
                    json.dump(chunk, out)
                file_count += 1
                chunk = []

        if chunk:
            out_file = split_dir / f"chunk_{file_count}.json"
            with open(out_file, 'w', encoding='utf-8') as out:
                json.dump(chunk, out)

    print(f"Splitting complete. {file_count + 1} chunk files created.")

    print("Inferring PostgreSQL column types based on a sample chunk...")
    sample_df = pd.read_json(split_dir / "chunk_0.json")
    
    def infer_pg_dtype(series):
        if pd.api.types.is_integer_dtype(series):
            return 'INTEGER'
        elif pd.api.types.is_float_dtype(series):
            return 'FLOAT'
        elif pd.api.types.is_bool_dtype(series):
            return 'BOOLEAN'
        elif pd.api.types.is_datetime64_any_dtype(series):
            return 'TIMESTAMP'
        else:
            return 'TEXT'
    
    column_types = {col: infer_pg_dtype(sample_df[col]) for col in sample_df.columns}
    
    print("\nInferred PostgreSQL Column Types:")
    for col, dtype in column_types.items():
        print(f"  - {col}: {dtype}")

    print("\nConverting chunk files to CSV format...")
    for json_file in tqdm(split_dir.glob("chunk_*.json"), desc="Converting", unit="file"):
        df = pd.read_json(json_file)
        df.to_csv(csv_dir / f"{json_file.stem}.csv", index=False)

    print("\nCSV files have been saved in the folder:", csv_dir)

    print("\nDownload links for generated CSV files:")
    for csv_file in csv_dir.glob("*.csv"):
        display(FileLink(csv_file))

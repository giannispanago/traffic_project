import pandas as pd
from pathlib import Path


INPUT_DIR = Path("output/results")
OUTPUT_FILE = INPUT_DIR / "all_vehicle_results.csv"


def merge_results():
    csv_files = sorted(
        f for f in INPUT_DIR.glob("clip_*_results.csv")
        if f.is_file()
    )

    if not csv_files:
        print("Δεν βρέθηκαν per-clip result CSV files.")
        raise SystemExit(1)

    dataframes = []

    for csv_file in csv_files:
        print(f"Reading: {csv_file}")
        df = pd.read_csv(csv_file, sep=";")
        df["source_file"] = csv_file.name
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df = merged_df[merged_df["speed_kmh"].notna()].copy()
    merged_df.to_csv(OUTPUT_FILE, index=False, sep=";")

    print(f"Merged {len(csv_files)} files.")
    print(f"Saved merged results to: {OUTPUT_FILE}")
    print(merged_df.head())


def main():
    merge_results()


if __name__ == "__main__":
    main()
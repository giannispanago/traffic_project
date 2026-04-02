import pandas as pd


CSV_PATH = "output/results/all_vehicle_results.csv"


def is_speeding(row):
    vehicle_class = str(row["class_name"]).lower()
    speed = row["speed_kmh"]

    if pd.isna(speed):
        return False

    if vehicle_class == "car":
        return speed > 90
    if vehicle_class in ["truck", "bus"]:
        return speed > 80

    return False


def generate_reports():
    df = pd.read_csv(CSV_PATH, sep=";")

    numeric_cols = ["line1_frame", "line2_frame", "crossing_frame", "time_sec", "window_5min", "speed_kmh"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df_direction = df[df["direction"].notna()].copy()
    df_speed = df[(df["direction"].notna()) & (df["speed_kmh"].notna())].copy()

    q1 = df_speed[["track_id", "class_name", "direction", "speed_kmh"]].copy()

    q2 = df_direction.groupby("direction").size().reset_index(name="vehicle_count")

    df_speed["is_speeding"] = df_speed.apply(is_speeding, axis=1)
    q3_by_direction = (
        df_speed[df_speed["is_speeding"]]
        .groupby("direction")
        .size()
        .reset_index(name="speeding_count")
    )

    q4 = df_speed[df_speed["speed_kmh"] > 130][
        ["track_id", "class_name", "direction", "speed_kmh", "time_sec", "window_5min"]
    ].copy()

    q5 = (
        df_direction.groupby(["window_5min", "direction"])
        .size()
        .reset_index(name="vehicle_count")
        .sort_values(["window_5min", "direction"])
    )

    q6 = (
        df_speed.groupby(["window_5min", "direction"])["speed_kmh"]
        .mean()
        .round()
        .astype(int)
        .reset_index(name="avg_speed_kmh")
        .sort_values(["window_5min", "direction"])
    )

    q1.to_csv("q1_speed_each_vehicle.csv", index=False, sep=";")
    q2.to_csv("q2_count_per_direction.csv", index=False, sep=";")
    q3_by_direction.to_csv("q3_speeding_by_direction.csv", index=False, sep=";")
    q4.to_csv("q4_alerts_over_130.csv", index=False, sep=";")
    q5.to_csv("q5_count_per_direction_per_5min.csv", index=False, sep=";")
    q6.to_csv("q6_avg_speed_per_direction_per_5min.csv", index=False, sep=";")

    print("Saved reports.")


def main():
    generate_reports()


if __name__ == "__main__":
    main()
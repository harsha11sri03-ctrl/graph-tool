import matplotlib.pyplot as plt
import pandas as pd
import re


def extract_time_from_row(row):
    try:
        row_str = " ".join(str(v) for v in row)
        match = re.search(r'\d{1,2}:\d{2}:\d{2}', row_str)

        if not match:
            return None

        h, m, s = map(int, match.group().split(":"))
        return h * 60 + m + s / 60

    except:
        return None


def detect_sequence_column(df):
    possible_names = ["sequence", "step", "seq", "id"]

    # ✅ direct match
    for col in df.columns:
        if col.lower() in possible_names:
            return col

    # ✅ numeric detection fallback
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors='coerce')
        if converted.notna().sum() > len(df) * 0.5:
            return col

    return None


def plot_bar(df):

    if df is None or df.empty:
        print("No data found")
        return

    # ✅ extract duration
    df["Duration_clean"] = df.apply(extract_time_from_row, axis=1)
    df = df.dropna(subset=["Duration_clean"])

    if df.empty:
        print("No valid duration data")
        return

    # ✅ remove summary rows
    df = df[~df.astype(str).apply(
        lambda row: row.str.contains("Total|Automation|Apps", case=False).any(), axis=1
    )]

    if df.empty:
        print("Only summary rows found")
        return

    # ✅ detect sequence column
    seq_col = detect_sequence_column(df)

    if seq_col:
        print(f"Using sequence column: {seq_col}")

        df[seq_col] = df[seq_col].replace("", pd.NA)
        df[seq_col] = df[seq_col].ffill()
        df[seq_col] = pd.to_numeric(df[seq_col], errors="coerce")

        df = df.dropna(subset=[seq_col])

        grouped_df = df.groupby(seq_col, as_index=False).first()
        grouped_df = grouped_df.sort_values(by=seq_col)

        x_values = grouped_df[seq_col]

    else:
        print("No sequence column → using row numbers")

        df = df.reset_index(drop=True)
        df["Sequence_auto"] = range(1, len(df) + 1)

        grouped_df = df
        x_values = grouped_df["Sequence_auto"]

    # ✅ convert to hours
    grouped_df["Duration_hours"] = grouped_df["Duration_clean"] / 60

    # ✅ plot
    plt.figure(figsize=(12, 6))

    bars = plt.bar(
        x_values.astype(int).astype(str),
        grouped_df["Duration_hours"],
        color='darkblue',
        width=0.4
    )

    plt.xlabel("Sequence")
    plt.ylabel("Duration (Hours)")

    plt.xticks(rotation=0)

    max_val = grouped_df["Duration_hours"].max()
    step = 0.5
    plt.yticks([i * step for i in range(int(max_val / step) + 2)])

    # ✅ add labels
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",
            ha='center',
            va='bottom',
            fontsize=8
        )

    plt.tight_layout()
    plt.show()

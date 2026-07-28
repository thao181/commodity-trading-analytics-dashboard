"""
Sinh dữ liệu mẫu cho 3 bảng:
  B. Internal Trading Data
  C. Internal Finance Data
  D. Internal Position Report

Dữ liệu có logic liên kết:
  - Mỗi giao dịch (Trading Data) có đúng 1 dòng thanh toán (Finance Data) qua Trade ID.
  - Position Report là số lũy kế (cumulative) Purchased/Sold Volume theo từng Commodity,
    tính đến cuối mỗi tháng, giống logic trong ảnh mẫu (Reported Position = Purchased - Sold).

Chạy: python generate_data.py
Kết quả: trading_data.xlsx, finance_data.xlsx, position_report.xlsx
"""

import random
from datetime import date, timedelta

import pandas as pd

random.seed(42)

# ---------------------------------------------------------------------------
# Cấu hình chung
# ---------------------------------------------------------------------------
START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 6, 30)  # không sinh giao dịch tháng 7/2026
N_TRADES = 100

COMMODITIES = {
    "Aluminum": (2200, 2550),
    "Copper": (8000, 9600),
    "Zinc": (2500, 3050),
    "Nickel": (15000, 18500),
    "Lead": (1900, 2250),
    "Tin": (24000, 27500),
}


def random_date(start: date, end: date) -> date:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def month_end(d: date) -> date:
    if d.month == 12:
        nxt = date(d.year + 1, 1, 1)
    else:
        nxt = date(d.year, d.month + 1, 1)
    return nxt - timedelta(days=1)


# ---------------------------------------------------------------------------
# B. Internal Trading Data
# ---------------------------------------------------------------------------
trades = []
for i in range(1, N_TRADES + 1):
    commodity = random.choice(list(COMMODITIES.keys()))
    lo, hi = COMMODITIES[commodity]
    trade_type = random.choices(["Buy", "Sell"], weights=[0.55, 0.45])[0]
    volume = random.choice(range(10, 210, 10))
    price = round(random.uniform(lo, hi), 1)
    trade_date = random_date(START_DATE, END_DATE)

    trades.append(
        {
            "Trade ID": f"T{i:04d}",
            "Date": trade_date,
            "Commodity": commodity,
            "Type": trade_type,
            "Volume": volume,
            "Contract Price": price,
        }
    )

df_trading = pd.DataFrame(trades).sort_values("Date").reset_index(drop=True)

# ---------------------------------------------------------------------------
# C. Internal Finance Data (1 dòng cash cho mỗi trade)
# ---------------------------------------------------------------------------
finance_rows = []
for i, row in df_trading.reset_index(drop=True).iterrows():
    settlement_date = row["Date"] + timedelta(days=random.randint(10, 20))
    cash_type = "Outflow" if row["Type"] == "Buy" else "Inflow"
    amount = round(row["Volume"] * row["Contract Price"], 2)

    if settlement_date <= END_DATE:
        status = random.choices(["Settled", "Pending"], weights=[0.85, 0.15])[0]
    else:
        status = "Pending"

    finance_rows.append(
        {
            "Cash ID": f"C{i + 1:03d}",
            "Trade ID": row["Trade ID"],
            "Settlement Date": settlement_date,
            "Cash Type": cash_type,
            "Amount": amount,
            "Status": status,
        }
    )

df_finance = pd.DataFrame(finance_rows)

# ---------------------------------------------------------------------------
# D. Internal Position Report
#    Lũy kế Purchased/Sold Volume theo Commodity, tính đến cuối mỗi tháng
# ---------------------------------------------------------------------------
months = sorted({month_end(d) for d in df_trading["Date"]})
position_rows = []
for commodity in COMMODITIES:
    df_c = df_trading[df_trading["Commodity"] == commodity]
    for m_end in months:
        purchased = df_c[(df_c["Type"] == "Buy") & (df_c["Date"] <= m_end)]["Volume"].sum()
        sold = df_c[(df_c["Type"] == "Sell") & (df_c["Date"] <= m_end)]["Volume"].sum()
        if purchased == 0 and sold == 0:
            continue
        position_rows.append(
            {
                "Date": m_end,
                "Commodity": commodity,
                "Purchased Volume": int(purchased),
                "Sold Volume": int(sold),
                "Reported Position": int(purchased - sold),
            }
        )

df_position = pd.DataFrame(position_rows).sort_values(["Date", "Commodity"]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# Xuất file Excel với format ngày dd/mm/yyyy
# ---------------------------------------------------------------------------
def save_xlsx(df: pd.DataFrame, path: str, date_cols):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        ws = writer.sheets["Sheet1"]
        for col_name in date_cols:
            col_idx = df.columns.get_loc(col_name) + 1
            for cell in ws.iter_rows(min_row=2, min_col=col_idx, max_col=col_idx, max_row=ws.max_row):
                cell[0].number_format = "DD/MM/YYYY"
        for i, col in enumerate(df.columns, 1):
            width = max(12, min(22, df[col].astype(str).map(len).max() + 2))
            ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = width


save_xlsx(df_trading, "trading_data.xlsx", ["Date"])
save_xlsx(df_finance, "finance_data.xlsx", ["Settlement Date"])
save_xlsx(df_position, "position_report.xlsx", ["Date"])

print(f"trading_data.xlsx: {len(df_trading)} dòng")
print(f"finance_data.xlsx: {len(df_finance)} dòng")
print(f"position_report.xlsx: {len(df_position)} dòng")

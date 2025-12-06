import os
import pandas as pd
from datetime import datetime

def export_reports_to_excel():
    results_path = "data/results/"
    reports_path = "data/reports/"
    export_dir = "data/exports/"
    os.makedirs(export_dir, exist_ok=True)

    export_file = os.path.join(export_dir, f"sentinel_reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")

    all_data = []
    for folder in [results_path, reports_path]:
        if not os.path.exists(folder):
            continue
        for root, _, files in os.walk(folder):
            for f in files:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                    all_data.append({"filename": f, "path": file_path, "content": content})
                except Exception as e:
                    all_data.append({"filename": f, "path": file_path, "content": f"Error reading: {e}"})

    if not all_data:
        print("⚠️ No reports found to export.")
        return

    df = pd.DataFrame(all_data)
    df.to_excel(export_file, index=False)
    print(f"✅ Exported {len(all_data)} reports to Excel: {export_file}")

    return export_file

# 📊 Graph Tool

A Python tool that reads Word and Excel files and generates bar graphs from deployment data.

---

## ✅ Features

- Supports Word (.docx)
- Supports Excel (.xlsx, .xls)
- Handles messy tables (merged rows, uneven structure)
- Automatically detects sequence/step column
- Extracts duration (HH:MM:SS format)
- Converts duration into Hours
- Generates clean bar graphs

---

## 📁 Project Structure
graph_tool/
│
├── main.py          # Runs the program
├── file_loader.py   # Reads input files
├── plotter.py       # Generates graph
├── requirements.txt # Dependencies
## ⚙️ Installation

Install required libraries:

```bash
pip install -r requirements.txt
▶️ Run the Project
python main.py
📌 How to Use

Run the program
File explorer will open
Select a Word or Excel file
Graph will be generated automatically

📊 Output

X-axis → Sequence / Step (auto detected)
Y-axis → Duration (in hours)
Handles grouped rows correctly
Removes summary rows (Total, etc.)


✅ Supported Files

Word (.docx)
Excel (.xlsx, .xls)
CSV
TXT

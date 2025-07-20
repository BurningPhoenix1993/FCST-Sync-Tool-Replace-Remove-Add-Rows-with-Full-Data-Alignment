# 📊 FCST Sync Tool – Replace, Remove & Add Rows

This is a **Streamlit-based FCST Sync Tool** that helps you synchronize forecast (FCST) data between two files:

✅ **Replace FCST** in the Base file (File1) when `LOC + ITEM + CHANNEL + FDATE` matches the Source file (File2).  
✅ **Remove rows** from Base that no longer exist in Source.  
✅ **Add new rows** from Source that are missing in Base.  
✅ **Preserves leading zeros and formatting**.  
✅ Generates a clean, **pipe-delimited CSV** ready for upload.  

---

## ✨ Features

- Match rows using a unique key: `LOC + ITEM + CHANNEL + FDATE`
- Replace only the `FCST` field for matched rows
- Remove obsolete rows from Base
- Add new rows from Source
- Pipe-delimited output, preserving original structure

---

## 🛠 Requirements

- **Python 3.9+**
- Libraries:
  - `streamlit`
  - `pandas`

You can install dependencies with:

```bash
pip install -r requirements.txt

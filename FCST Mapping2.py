import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📊 FCST Sync (Replace + Add + Remove)", layout="centered")
st.title("🔁 Sync Base File with Source (Replace, Remove & Add)")

st.markdown("""
This tool will:
1️⃣ **Replace FCST** in Base (File1) where LOC+ITEM+CHANNEL+FDATE matches Source (File2)  
2️⃣ **Remove rows from Base** that are not present in Source  
3️⃣ **Add new rows from Source** that are missing in Base  

✅ Leading zeros & formatting are preserved.  
✅ Output is a clean, pipe-delimited file.
""")

# File uploaders
file1 = st.file_uploader("📂 Upload File 1 (Base)", type=["csv", "txt"])
file2 = st.file_uploader("📂 Upload File 2 (Source)", type=["csv", "txt"])

if file1 and file2:
    try:
        # --- Read File 1 (Base) ---
        file1_lines = file1.read().decode("utf-8").splitlines()
        header = file1_lines[0].strip()
        col_names = header.split("|")
        data1 = [line.split("|") for line in file1_lines[1:]]
        df1 = pd.DataFrame(data1, columns=col_names)

        # --- Read File 2 (Source) ---
        df2 = pd.read_csv(file2, delimiter='|', dtype=str, keep_default_na=False)

        # --- Create unique KEY ---
        df1['KEY'] = df1['LOC'].str.strip() + df1['ITEM'].str.strip() + df1['CHANNEL'].str.strip() + df1['FDATE'].str.strip()
        df2['KEY'] = df2['LOC'].str.strip() + df2['ITEM'].str.strip() + df2['CHANNEL'].str.strip() + df2['FDATE'].str.strip()

        # --- Replace FCST for matching keys ---
        fcst_map = df2.set_index('KEY')['FCST'].to_dict()
        df1['FCST'] = df1.apply(lambda row: fcst_map.get(row['KEY'], row['FCST']), axis=1)

        # --- Keep only keys present in Source ---
        df1_filtered = df1[df1['KEY'].isin(df2['KEY'])].copy()

        # --- Find new records in Source that are NOT in Base ---
        new_rows = df2[~df2['KEY'].isin(df1['KEY'])].copy()

        # --- Combine (Filtered Base + New Source Rows) ---
        df_final = pd.concat([df1_filtered, new_rows], ignore_index=True)

        # Drop helper KEY column
        df_final.drop(columns=['KEY'], inplace=True)

        # --- Reconstruct pipe-delimited output ---
        output_lines = ['|'.join(col_names)]
        for _, row in df_final.iterrows():
            output_lines.append('|'.join(row.astype(str)))

        result_data = '\n'.join(output_lines)

        # --- Streamlit Output ---
        st.success("✅ FCST Synced: Replaced, Removed Missing, and Added New!")
        st.download_button("📥 Download Synced CSV", result_data, file_name="fcst_synced.csv", mime="text/csv")

        st.text("🔍 Preview:")
        st.code('\n'.join(output_lines[:10]), language='text')

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Upload both files to proceed.")

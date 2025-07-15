import streamlit as st
import pandas as pd

# Load CSV files
@st.cache_data
def load_data():
    # Load LED component files
    led_lightunit_df = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv", skiprows=2, header=None)
    led_lenscolor_df = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv")
    led_voltage_df = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv")

    # Build lookup dictionaries
    lightunit_lookup = {str(v).strip(): str(k).strip() for k, v in zip(led_lightunit_df[0], led_lightunit_df[1])}
    lenscolor_lookup = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_lenscolor_df.iterrows()}
    voltage_lookup = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_voltage_df.iterrows()}

    return lightunit_lookup, lenscolor_lookup, voltage_lookup

lightunit_lookup, lenscolor_lookup, voltage_lookup = load_data()

# UI
st.title("🔍 10250T Illuminated (LED) Catalog Number Decoder")

catalog_input = st.text_input("Enter a 10250T LED catalog number (e.g., 10250T397LRD06-53):")

if catalog_input:
    normalized = catalog_input.replace("-", "").strip().upper()

    if normalized.startswith("10250T") and len(normalized) > 12:
        code_part = normalized[6:]
        lightunit_code = code_part[:4]  # e.g., 397L
        lens_code = code_part[4:6]      # e.g., RD
        voltage_code = code_part[6:8]   # e.g., 06
        circuit_code = code_part[8:]    # e.g., 53

        lightunit_label = lightunit_lookup.get(lightunit_code, "Unknown Light Unit")
        lens_label = lenscolor_lookup.get(lens_code, "Unknown Lens Color")
        voltage_label = voltage_lookup.get(voltage_code, "Unknown Voltage")

        lightunit_pn = f"10250T{lightunit_code}"
        lens_pn = f"10250T{lens_code}"
        voltage_pn = f"10250T{voltage_code}"
        circuit_pn = f"10250T{circuit_code}"

        st.markdown("### ✅ Decoded Result")
        st.write(f"**Light Unit**: {lightunit_label}")
        st.write(f"**Lens Color**: {lens_label}")
        st.write(f"**Voltage**: {voltage_label}")
        st.write(f"**Circuit**: {circuit_code}")

        st.markdown("### 🧩 Component Part Numbers")
        st.write(f"**Light Unit P/N**: `{lightunit_pn}`")
        st.write(f"**Lens Color P/N**: `{lens_pn}`")
        st.write(f"**Circuit P/N**: `{circuit_pn}`")
    else:
        st.error("Catalog number must start with '10250T' and be long enough to decode.")

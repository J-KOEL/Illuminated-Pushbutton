import streamlit as st
import pandas as pd

# Load CSV files
@st.cache_data
def load_data():
    # LED files
    led_light_unit_df = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv", header=None, names=["Label", "Code"], usecols=[0, 1], skiprows=1)
    led_lens_color_df = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv", header=None, names=["Label", "Code"], usecols=[0, 1], skiprows=1)
    led_voltage_df = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv", header=None, names=["Label", "Code"], usecols=[0, 1], skiprows=1)

    # Incandescent files
    inc_light_unit_df = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit.csv", header=None, names=["Label", "Code"], usecols=[0, 1], skiprows=1)
    inc_lens_color_df = pd.read_csv("illuminatedPushbuttonIncandescentLensColor.csv", header=None, names=["Label", "Code"], usecols=[0, 1], skiprows=1)

    # Circuit file
    circuit_df = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None, names=["Label", "Code"], usecols=[0, 1], skiprows=1)

    # Create lookup dictionaries
    led_light_unit = {row["Code"].strip(): row["Label"].strip() for _, row in led_light_unit_df.iterrows()}
    led_lens_color = {row["Code"].strip(): row["Label"].strip() for _, row in led_lens_color_df.iterrows()}
    led_voltage = {row["Code"].strip(): row["Label"].strip() for _, row in led_voltage_df.iterrows()}

    inc_light_unit = {row["Code"].strip(): row["Label"].strip() for _, row in inc_light_unit_df.iterrows()}
    inc_lens_color = {row["Code"].strip(): row["Label"].strip() for _, row in inc_lens_color_df.iterrows()}

    circuit_lookup = {row["Code"].strip(): row["Label"].strip() for _, row in circuit_df.iterrows()}

    return led_light_unit, led_lens_color, led_voltage, inc_light_unit, inc_lens_color, circuit_lookup

# Load data
led_light_unit, led_lens_color, led_voltage, inc_light_unit, inc_lens_color, circuit_lookup = load_data()

# UI
st.title("💡 Illuminated Pushbutton Catalog Decoder")

catalog_input = st.text_input("Enter a 10250T catalog number (e.g., 10250T397LRD24-1):")

if catalog_input:
    normalized = catalog_input.replace("-", "").strip().upper()

    if normalized.startswith("10250T") and len(normalized) > 8:
        code_part = normalized[6:]

        # Try LED first (light unit code is 4 chars and ends with 'L')
        light_unit_code = code_part[:4]
        if light_unit_code in led_light_unit:
            lens_color_code = code_part[4:6]
            voltage_code = code_part[6:8]
            circuit_code = code_part[8:]

            st.markdown("### ✅ Decoded Result (LED)")
            st.write(f"**Light Unit**: {led_light_unit.get(light_unit_code, 'Unknown')}")
            st.write(f"**Lens Color**: {led_lens_color.get(lens_color_code, 'Unknown')}")
            st.write(f"**LED Voltage**: {led_voltage.get(voltage_code, 'Unknown')}")
            st.write(f"**Circuit Type**: {circuit_lookup.get(circuit_code, 'Unknown')}")

        else:
            # Try Incandescent (light unit code is 3 chars)
            light_unit_code = code_part[:3]
            lens_color_code = code_part[3:6]
            circuit_code = code_part[6:]

            if light_unit_code in inc_light_unit:
                st.markdown("### ✅ Decoded Result (Incandescent)")
                st.write(f"**Light Unit**: {inc_light_unit.get(light_unit_code, 'Unknown')}")
                st.write(f"**Lens Color**: {inc_lens_color.get(lens_color_code, 'Unknown')}")
                st.write(f"**Circuit Type**: {circuit_lookup.get(circuit_code, 'Unknown')}")
            else:
                st.error("Unrecognized light unit code.")
    else:
        st.error("Catalog number must start with '10250T' and be long enough to decode.")

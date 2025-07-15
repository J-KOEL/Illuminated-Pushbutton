import streamlit as st
import pandas as pd
import re

@st.cache_data
def load_data():
    inc_lens = pd.read_csv("illuminatedPushbuttonIncandescentLensColor.csv", header=None)
    inc_light = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit.csv", header=None)
    circuit = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None)
    led_lens = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv", header=0)
    led_light = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv", skiprows=2, header=None)
    led_volt = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv", header=0)

    inc_lens_map = {str(code).strip(): str(label).strip() for label, code in zip(inc_lens[0], inc_lens[1])}
    inc_light_map = {str(code).strip(): str(label).strip() for label, code in zip(inc_light[0], inc_light[1])}
    circuit_map = {str(code).strip(): str(label).strip() for label, code in zip(circuit[0], circuit[1])}
    led_lens_map = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_lens.iterrows()}
    led_light_map = {str(code).strip(): str(label).strip() for label, code in zip(led_light[0], led_light[1])}
    led_volt_map = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_volt.iterrows()}

    return inc_lens_map, inc_light_map, circuit_map, led_lens_map, led_light_map, led_volt_map

inc_lens_map, inc_light_map, circuit_map, led_lens_map, led_light_map, led_volt_map = load_data()

st.title("💡 Illuminated Pushbutton Decoder")

catalog_input = st.text_input("Enter a 10250T catalog number (e.g., 10250T397LRD06-53 or 10250T416C21-51):")

def decode_led(pn):
    match = re.match(r"(10250T)(\d{3}L)([A-Z]{2})([0-9A-Z]{2})-(\d{2})", pn)
    if not match:
        return None, "Regex match failed"
    series, lightunit, lens, voltage, circuit = match.groups()
    debug_info = {
        "Series": series,
        "Light Unit Code": lightunit,
        "Lens Code": lens,
        "Voltage Code": voltage,
        "Circuit Code": circuit,
        "Light Unit Found": lightunit in led_light_map,
        "Lens Found": lens in led_lens_map,
        "Voltage Found": voltage in led_volt_map,
        "Circuit Found": circuit in circuit_map
    }
    return {
        "Series": series,
        "Light Unit": f"{lightunit} → {led_light_map.get(lightunit, 'Unknown')}",
        "Lens Color": f"{lens} → {led_lens_map.get(lens, 'Unknown')}",
        "Voltage": f"{voltage} → {led_volt_map.get(voltage, 'Unknown')}",
        "Circuit": f"{circuit} → {circuit_map.get(circuit, 'Unknown')}",
        "Full Part Number": f"{series}{lightunit}{lens}{voltage}-{circuit}"
    }, debug_info

def decode_incandescent(pn):
    match = re.match(r"(10250T)(\d{3})(C\d{2})-(\d{2})", pn)
    if not match:
        return None, "Regex match failed"
    series, lightunit, lens, circuit = match.groups()
    debug_info = {
        "Series": series,
        "Light Unit Code": lightunit,
        "Lens Code": lens,
        "Circuit Code": circuit,
        "Light Unit Found": lightunit in inc_light_map,
        "Lens Found": lens in inc_lens_map,
        "Circuit Found": circuit in circuit_map
    }
    return {
        "Series": series,
        "Light Unit": f"{lightunit} → {inc_light_map.get(lightunit, 'Unknown')}",
        "Lens Color": f"{lens} → {inc_lens_map.get(lens, 'Unknown')}",
        "Circuit": f"{circuit} → {circuit_map.get(circuit, 'Unknown')}",
        "Full Part Number": f"{series}{lightunit}{lens}-{circuit}"
    }, debug_info

if catalog_input:
    normalized = catalog_input.strip().upper()
    if "L" in normalized:
        decoded, debug = decode_led(normalized)
        type_detected = "LED"
    else:
        decoded, debug = decode_incandescent(normalized)
        type_detected = "Incandescent"

    if decoded:
        st.subheader(f"Detected Type: {type_detected}")
        st.write("### 🔍 Decoded Components")
        for key, value in decoded.items():
            st.write(f"**{key}:** {value}")
        st.write("### 🐞 Debug Info")
        for key, value in debug.items():
            st.write(f"{key}: {value}")
    else:
        st.error("Invalid part number format or unknown components.")
        if isinstance(debug, str):
            st.text(f"Debug: {debug}")

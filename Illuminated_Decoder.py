# Regenerate the Streamlit app using corrected column indices for LED lens and voltage files

import streamlit as st
import pandas as pd
import re

@st.cache_data
def load_data():
    inc_lens = pd.read_csv("illuminatedPushbuttonIncandescentLensColor.csv", header=None)
    inc_light = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit.csv", header=None)
    circuit = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None)
    led_lens = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv", header=None)
    led_light = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv", header=None)
    led_volt = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv", header=None)

    inc_lens_map = {str(v).strip(): str(k).strip() for k, v in zip(inc_lens[1], inc_lens[0])}
    inc_light_map = {str(v).strip(): str(k).strip() for k, v in zip(inc_light[1], inc_light[0])}
    circuit_map = {str(v).strip(): str(k).strip() for k, v in zip(circuit[1], circuit[0])}
    led_lens_map = {str(v).strip(): str(k).strip() for k, v in zip(led_lens[1], led_lens[0])}
    led_light_map = {str(v).strip(): str(k).strip() for k, v in zip(led_light[1][2:], led_light[0][2:])}
    led_volt_map = {str(v).strip(): str(k).strip() for k, v in zip(led_volt[1], led_volt[0])}

    return inc_lens_map, inc_light_map, circuit_map, led_lens_map, led_light_map, led_volt_map

inc_lens_map, inc_light_map, circuit_map, led_lens_map, led_light_map, led_volt_map = load_data()

st.title("💡 Illuminated Pushbutton Decoder")

catalog_input = st.text_input("Enter a 10250T catalog number (e.g., 10250T397LRD06-53 or 10250T416C21-51):")

def decode_led(pn):
    match = re.match(r"(10250T)(\\d{3}L)([A-Z]{2})([0-9A-Z]{2})-(\\d{2})", pn)
    if not match:
        return None
    series, lightunit, lens, voltage, circuit = match.groups()
    return {
        "Series": series,
        "Light Unit": f"{lightunit} → {led_light_map.get(lightunit, 'Unknown')}",
        "Lens Color": f"{lens} → {led_lens_map.get(lens, 'Unknown')}",
        "Voltage": f"{voltage} → {led_volt_map.get(voltage, 'Unknown')}",
        "Circuit": f"{circuit} → {circuit_map.get(circuit, 'Unknown')}",
        "Operator P/N": f"{series}{lightunit}{lens}",
        "Contact Block P/N": f"{series}{circuit}"
    }

def decode_incandescent(pn):
    match = re.match(r"(10250T)(\\d{3})(C\\d{2})-(\\d{2})", pn)
    if not match:
        return None
    series, lightunit, lens, circuit = match.groups()
    return {
        "Series": series,
        "Light Unit": f"{lightunit} → {inc_light_map.get(lightunit, 'Unknown')}",
        "Lens Color": f"{lens} → {inc_lens_map.get(lens, 'Unknown')}",
        "Circuit": f"{circuit} → {circuit_map.get(circuit, 'Unknown')}",
        "Operator P/N": f"{series}{lightunit}{lens}",
        "Contact Block P/N": f"{series}{circuit}"
    }

if catalog_input:
    normalized = catalog_input.strip().upper()
    if "L" in normalized:
        decoded = decode_led(normalized)
        type_detected = "LED"
    else:
        decoded = decode_incandescent(normalized)
        type_detected = "Incandescent"

    if decoded:
        st.subheader(f"Detected Type: {type_detected}")
        st.write("### 🔍 Decoded Components")
        for key, value in decoded.items():
            st.write(f"**{key}:** {value}")
    else:
        st.error("Invalid part number format or unknown components.")

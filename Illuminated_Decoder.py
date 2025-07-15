import streamlit as st
import pandas as pd
import re

# Load mapping files
incandescent_lens_df = pd.read_csv("illuminatedPushbuttonIncandescentLensColor.csv")
incandescent_lightunit_df = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit.csv")
circuit_df = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv")

led_lens_df = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv")
led_lightunit_df = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv", skiprows=1)
led_voltage_df = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv")

# Create dictionaries for quick lookup
incandescent_lens_map = dict(zip(incandescent_lens_df['Code'].str.strip(), incandescent_lens_df['Label'].str.strip()))
incandescent_lightunit_map = dict(zip(incandescent_lightunit_df['Code'].str.strip(), incandescent_lightunit_df['Label'].str.strip()))
circuit_map = dict(zip(circuit_df['Code'].str.strip(), circuit_df['Label'].str.strip()))

led_lens_map = dict(zip(led_lens_df['Code'].str.strip(), led_lens_df['Label'].str.strip()))
led_lightunit_map = dict(zip(led_lightunit_df['Code'].str.strip(), led_lightunit_df['Label'].str.strip()))
led_voltage_map = dict(zip(led_voltage_df['Code'].str.strip(), led_voltage_df['Label'].str.strip()))

# Streamlit UI
st.title("Illuminated Pushbutton Part Number Decoder")

part_number = st.text_input("Enter full part number (e.g., 10250T397LRD06-53):")

def decode_led(pn):
    match = re.match(r"(10250T)(\d{3}L)([A-Z]{2})([0-9A-Z]{2})-(\d{2})", pn)
    if not match:
        return None
    series, lightunit, lens, voltage, circuit = match.groups()
    return {
        "Series": series,
        "Light Unit": f"{lightunit} → {led_lightunit_map.get(lightunit, 'Unknown')}",
        "Lens Color": f"{lens} → {led_lens_map.get(lens, 'Unknown')}",
        "Voltage": f"{voltage} → {led_voltage_map.get(voltage, 'Unknown')}",
        "Circuit": f"{circuit} → {circuit_map.get(circuit, 'Unknown')}"
    }

def decode_incandescent(pn):
    match = re.match(r"(10250T)(\d{3})(C\d{2})-(\d{2})", pn)
    if not match:
        return None
    series, lightunit, lens, circuit = match.groups()
    return {
        "Series": series,
        "Light Unit": f"{lightunit} → {incandescent_lightunit_map.get(lightunit, 'Unknown')}",
        "Lens Color": f"{lens} → {incandescent_lens_map.get(lens, 'Unknown')}",
        "Circuit": f"{circuit} → {circuit_map.get(circuit, 'Unknown')}"
    }

if part_number:
    if "L" in part_number:
        decoded = decode_led(part_number)
        type_detected = "LED"
    else:
        decoded = decode_incandescent(part_number)
        type_detected = "Incandescent"

    if decoded:
        st.subheader(f"Detected Type: {type_detected}")
        st.write("### Decoded Components")
        for key, value in decoded.items():
            st.write(f"**{key}:** {value}")
    else:
        st.error("Invalid part number format or unknown components.")

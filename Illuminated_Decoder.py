import streamlit as st
import pandas as pd

st.title("10250T Catalog Code Tables")

# Load CSVs
led_light_unit = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv")
led_lens_color = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv")
led_voltage = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv")

inc_light_unit = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit.csv", skiprows=1, usecols=[0, 1], names=["Label", "Code"])
inc_lens_color = pd.read_csv("illuminatedPushbuttonIncandescentLensColor.csv", skiprows=1, usecols=[0, 1], names=["Label", "Code"])

circuit = pd.read_csv("NonIlluminatedPushbuttonCircuit 4.csv", skiprows=1, usecols=[0, 1], names=["Label", "Code"])

# Display tables
st.header("🔌 LED Light Unit Codes")
st.dataframe(led_light_unit[["Label", "Code"]])

st.header("🎨 LED Lens Color Codes")
st.dataframe(led_lens_color)

st.header("⚡ LED Voltage Codes")
st.dataframe(led_voltage)

st.header("🔥 Incandescent Light Unit Codes")
st.dataframe(inc_light_unit)

st.header("🌈 Incandescent Lens Color Codes")
st.dataframe(inc_lens_color)

st.header("⚙️ Circuit Type Codes")
st.dataframe(circuit)

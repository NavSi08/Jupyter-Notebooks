import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.header('Head distribution in homogeneous media')
st.subheader('Heads in water and sand')

# --- Settings ---
base_level_ini = 0.     # cm (bottom of bucket)
top_level_max = 100.
top_level_ini = 50.
# Initialize for the first time
if "top_level" not in st.session_state:
    st.session_state.top_level = 50.0
if "base_level" not in st.session_state:
    st.session_state.base_level = 0.0
if "z_measure" not in st.session_state:
    st.session_state.z_measure = 0.0

# --- Input slider ---
column1 = st.columns((1,1), gap = 'large')
with column1[0]:
    st.slider(':blue[**Filling level**]', 0.0, top_level_max, top_level_ini, 1.0, key="top_level")
    st.slider('**Bucket bottom level**', 0.0, top_level_max, base_level_ini, 1.0, key="base_level")
    sand = st.toggle('Bucket filled with sand and water')

with column1[1]:
    st.slider(':red[**Elevation of measurement $z_{measure}$**]', 0.0, top_level_max, 0.0, 0.1,key="z_measure")

# Use values from session state
top_level = st.session_state.top_level
base_level = st.session_state.base_level
z_measure = st.session_state.z_measure

# --- Generate vertical profile ---
z = np.linspace(0, top_level, 100)  # Full vertical profile

# --- Calculate head components ---
elevation_head = z
pressure_head = np.where(elevation_head >= base_level, top_level - elevation_head, np.nan)
total_head = np.where(elevation_head >= base_level, pressure_head + elevation_head, np.nan)

if (z_measure >= base_level):
    pressure_head_measure = top_level - z_measure
    total_head_measure = pressure_head_measure + z_measure
else:
    pressure_head_measure = 0
    total_head_measure = 0

# PLOT HERE
# --- Create side-by-side plots ---
fig, (ax_bucket, ax_profile) = plt.subplots(1, 2, figsize=(10, 6), width_ratios=[1, 2])

# --- Left: Water column (bucket) ---
bucket_width = 4  # cm
water_left = 0
water_right = bucket_width

# Water fill
z_fill = np.linspace(base_level, top_level, 100)

if sand:
    ax_bucket.fill_betweenx(z_fill, water_left, water_right, color='brown', alpha=0.7)
else:
    ax_bucket.fill_betweenx(z_fill, water_left, water_right, color='lightblue', alpha=0.7)

# Bucket outline (left, right, bottom)
ax_bucket.plot([water_left, water_left], [base_level, top_level_max], color='black', linewidth=4)  # left wall
ax_bucket.plot([water_right, water_right], [base_level, top_level_max], color='black', linewidth=4)  # right wall
ax_bucket.plot([water_left, water_right], [base_level, base_level], color='black', linewidth=4)  # bottom line

# Triangle marker at water table (like ∇)
ax_bucket.plot(
    [(water_left + water_right) / 5],
    [top_level+2],
    marker='v',
    color='navy',
    markersize=10
)
# Horizontal lines below triangle
line_y1 = top_level - 2  # slightly below triangle
line_y2 = top_level - 4  # a bit further down

line_length = 0.2
x_center = (water_left + water_right) / 5

# First line
ax_bucket.plot(
    [x_center - line_length, x_center + line_length],
    [line_y1, line_y1],
    color='navy',
    linewidth=1.5
)

# Second line
ax_bucket.plot(
    [x_center - line_length * 0.6, x_center + line_length * 0.6],
    [line_y2, line_y2],
    color='navy',
    linewidth=1.5
)

# Pressure sensor at z_measure (like *)
# TODO ALSO CONSIDER SENSOR BELOW BOTTOM
if base_level <= z_measure <= top_level:
    ax_bucket.plot(
        [(water_left + water_right) / 1.1],
        [z_measure],
        marker='o',
        color='red',
        markersize=10
    )
    ax_bucket.plot([((water_left + water_right) / 1.1), ((water_left + water_right) / 1.1)], [z_measure, top_level], color='black', linewidth=1,linestyle='--')  # line of measurement sensor
else:
    ax_bucket.plot(
        [(water_left + water_right) / 1.1],
        [z_measure],
        marker='o',
        color='lightgrey',
        markersize=10
    )
    ax_bucket.plot([((water_left + water_right) / 1.1), ((water_left + water_right) / 1.1)], [z_measure, top_level], color='lightgrey', linewidth=1,linestyle='--')  # line of measurement sensor
    ax_bucket.text(
        (water_left + water_right) / 1.3,
        top_level+10,
        "Measurment \noutside the \nWater filled \nbucket",
        fontsize=12,
        color='red',
        ha='center',
        va='center',
    )
    
# Text label
if sand:
    ax_bucket.text(
        (water_left + water_right) / 2,
        base_level + 5,
        "Sand filled\nbucket",
        fontsize=12,
        color='black',
        ha='center',
        va='center',
        fontweight='bold'
    )
else:
    ax_bucket.text(
        (water_left + water_right) / 2,
        base_level + 5,
        "Water filled\nbucket",
        fontsize=12,
        color='navy',
        ha='center',
        va='center',
        fontweight='bold'
    )

# Finalize bucket plot
ax_bucket.set_xlim(0, bucket_width)
ax_bucket.set_ylim(0, top_level_max)
ax_bucket.axis('off')
ax_bucket.set_title("Water Column", fontsize=12)

# --- Right: Head components ---
ax_profile.plot(elevation_head, z, label="Elevation Head (z)", color='grey')
ax_profile.plot(pressure_head, z, label="Pressure Head (ψ)", color='orange')
ax_profile.plot(total_head, z, label="Total Head (h)", color='blue')
if (z_measure <= top_level):
    ax_profile.plot(z_measure, z_measure, 'o', color='grey')
if base_level <= z_measure <= top_level:
    ax_profile.plot(pressure_head_measure, z_measure, 'ro')
    ax_profile.plot(total_head_measure, z_measure, 'o', color='blue')

ax_profile.set_xlabel("Head [cm]")
ax_profile.set_ylabel("Elevation [cm]")
ax_profile.set_xlim(0, top_level_max + 5)
ax_profile.set_ylim(0, top_level_max)
ax_profile.set_title("Hydraulic Head Components")
#ax_profile.grid(True)
ax_profile.legend()

# --- Display in Streamlit ---
st.pyplot(fig)
st.write('**Your pressure transducer measure:**')
if (z_measure >= base_level):
    st.write(':orange[**Pressure head**] (in cm) = %5.1f' %pressure_head_measure)
else:
    st.write(':orange[**Pressure head**] (in cm) = n. a. (Sensor below bottom)')
st.write(':grey[**Elevation head**] (in cm) =%5.1f' %z_measure)
if (z_measure >= base_level):
    st.write(':blue[**Total head**] (in cm) = %5.1f' %(pressure_head_measure+z_measure))
else:
    st.write(':blue[**Total head**] (in cm) = n. a. (Sensor below bottom)')
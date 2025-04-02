# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import io
import pandas as pd
import streamlit as st
from streamlit_extras.stodo import to_do

### 01 TITLE AND HEADER

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
   #"Colleague Name": [1],  # Author 2 also belongs to Institution 1
}
institutions = {
    1: "TU Dresden",
#   2: "Second Institution / Organization"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)  # Institutions in one line

st.title('🎯 The Theis solution for pumping test evaluation')

st.header(':blue[Manually fit parameter values via type-curve matching]')

st.subheader(':blue-background[Materials and Guidance for Theis Type-curve matching]', divider="blue")

### 02 INITIAL EXPLANATION
st.markdown('''
            Transient Flow toward a well in a confined aquifer is described here using the Theis Solution. You can use the subsequent materials and instructions to perform manual type-curve matching.
            '''
)

st.subheader(':blue-background[The Theis type-curve]', divider="blue")
st.markdown('''
            The **Theis type curve plot** is a fundamental tool in hydrogeology for analyzing **transient groundwater flow** in response to well pumping. It is based on the **Theis solution**, which describes how drawdown increases with time around a well that is pumping groundwater from a **confined aquifer**.
            
            Plotting **dimensionless drawdown** against **dimensionless time** on a logarithmic scale, creates the **Theis Type Curve** which provides a theoretical reference for evaluating aquifer properties. This approach is widely used to estimate **transmissivity ($T$)** and **storativity ($S$)** by plotting field measurements of drawdown versus time at locations near a pumping well and **aligning the field-data curve to the Theis type curve with the axes of both graphs parallel**.
            
            Once the curves are aligned, **a match point is selected**. The point can be any corresponding point on the graphs of the theoretical and measured-data curves. That is, it need not be at a location on the curves themselves. This is the case because, when the curves are aligned, any point will have the same ratio of associated values on the axes of the theoretical and the field graph. **Typically**, the match point is selcted **where the values on the axes of the theoretical curve are simple round numbers (e.g., 1, 10, or 100)** to make calculations easier and reduce error in reading values from the graphs, thus reduce error in estimating the parameter values.
            
            The first graph below, is the **Theis type curve. You can select a point that will be used to correspond to a point on a graph of field measured drawdown versus time**. You also have the option to download the figure for further study.  
            '''
)
### 03 INITIAL ASSESSMENTS

### 04 THEORY

### 05 FUNCTIONS

#Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)

def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u

def theis_s(Q, T, u):
    s = Q / 4. / np.pi / T * well_function(u)
    return s

def theis_wu(Q, T, s):
    wu = s * 4. * np.pi * T / Q
    return wu

def deriv(t, tm, s, sm):
    #d = (s-sm)/(np.log(t)-np.log(tm))
    d=((t+tm)/2)*((s-sm)/(t-tm))
    return d
    
# Data for the type curve plot
u_max = 10
r_max = 1000000
u  = [u_max for x in range(r_max)]
um = [u_max for x in range(r_max)]
u_inv  = [r_max/u_max for x in range(r_max)]
um_inv = [r_max/u_max for x in range(r_max)]
w_u  = [well_function(u_max/r_max) for x in range(r_max)]
w_um = [well_function(u_max/r_max) for x in range(r_max)]


### 07 COMPUTATION
#for x in range(1,r_max,1):
#    if x>0:
#        u[x] = x*u_max/r_max
#        u_inv[x] = 1/u[x]
#        w_u[x] = well_function(u[x])
    
# Define parameters
num_points = 100  # Adjust for desired resolution
u_min = 1e-6  # Set a small minimum u value to avoid division by zero
u_max = 10    # Adjust u_max based on problem constraints

# Use log-spaced values to cover a wide range efficiently
u = np.geomspace(u_min, u_max, num=num_points)  # Log-spaced values of u
u_inv = 1 / u
w_u = well_function(u)  # Assuming well_function is vectorized
    
### 08 PLOTTING
# Plotting the Theis curve

#W(u) is match_wu and 1/u is match_uinv

u_inv_values = [0.1, 1.0, 10, 100, 1000]
wu_values = [0.01, 0.1, 1.0, 10]

columns1 = st.columns((1,1), gap = 'large')
with columns1[0]:
    match_u_inv = st.select_slider('Select 1/u for the matchpoint', options= u_inv_values, value=1.0)
with columns1[1]:
    match_wu     =st.select_slider('Select W(u) for the matchpoint', options= wu_values, value=1.0)
        
matchgrid_x=[match_u_inv, match_u_inv]
matchgrid_y=[match_wu, match_wu]
matchgrid  =[0.001, 1000000]

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)  # adjust plot area
ax.plot(u_inv, w_u, color = 'black', linewidth = 2)
ax.plot(match_u_inv, match_wu,'bo',markersize=6)
ax.plot(matchgrid_x,matchgrid,color ='lime', linewidth = 1)
ax.plot(matchgrid,matchgrid_y,color = 'lime', linewidth = 1)
plt.yscale("log")
plt.xscale("log")
plt.axis([0.1,1E4,1E-2,1E+1])
ax.set(xlabel='1/u', ylabel='w(u)',
       title='Theis type curve for manual evaluation')
ax.grid(which="both",color='whitesmoke', linewidth=0.5)
ax.spines['top'].set_color('lightgrey')
ax.spines['bottom'].set_color('lightgrey')
ax.spines['right'].set_color('lightgrey')
ax.spines['left'].set_color('lightgrey')
ax.tick_params(which='both', colors='lightgrey')

st.pyplot(fig)

# Safe the figure
img_buffer = io.BytesIO()
fig.savefig(img_buffer, format="png", dpi=300)
img_buffer.seek(0)  # Reset buffer position

columns5 = st.columns((1,1,1), gap = 'large')
with columns5[1]:
    # Add download button
    st.download_button(
        label=":green[**Download**] **Theis Type Curve**",
        data=img_buffer,
        file_name="Theis_type_curve.png",
        mime="image/png"
        )
        
# PLOTTING DATA

st.subheader(':blue-background[Loading and plotting measured data]', divider="blue")
st.markdown('''
            To analyze field data with the **Theis type curve**, you can either **upload your own dataset** or use a **predefined measurement data**. Once the data are loaded, you have the option to **download the dataset to print for manual curve matching**. The plot can be displayed using **linear or semi-logarithmic axes**, allowing for flexible visualization of the drawdown behavior.  
            '''
)

### 06 READ AND PREPARE DATA

# TODO ALLOW CSV / MORE DATA (RANDOM GENERATED)
# Select data and solution
columns12 = st.columns((1,1), gap = 'large')
with columns12[0]:
    datasource = st.selectbox("**What data should be used?**",
    ("Synthetic textbook data", "Load own CSV dataset"), key='Data')
if (datasource == "Synthetic textbook data"):
    # Data and parameter from SYMPLE exercise
    m_time = [1,1.5,2,2.5,3,4,5,6,8,10,12,14,18,24,30,40,50,60,100,120] # time in minutes
    m_ddown = [0.66,0.87,0.99,1.11,1.21,1.36,1.49,1.59,1.75,1.86,1.97,2.08,2.20,2.36,2.49,2.65,2.78,2.88,3.16,3.28]   # drawdown in meters
    r = 120       # m
    b = 8.5       # m
    Qs = 0.3/60   # m^3/s
    Qd = Qs*60*60*24 # m^3/d
    st.write('**Pumping rate (m³/s)** for the **pumping test** = % 5.3f'% Qs)
    st.write('**Distance (m)** from the **well** for the **observation** =  % 6.2f'% r)
    st.write('**average Aquifer thickness** (m) = % 6.2f'% b)
elif(st.session_state.Data =="Load own CSV dataset"):
    # Initialize
    m_time = []
    m_ddown = []
    r = 100       # m
    b = 10        # m
    Qs = 0.005    # m^3/s
    Qd = 100      # m^3/d
    uploaded_file = st.file_uploader("Choose a file (subsequently you can add the aquifer thicknes, the pumping rate and the distance between well and observation). The required data format for the CSV-file is time in minutes and drawdown in meters, both separated by a comma.")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        m_time = list(df.iloc[:,0].values)
        m_ddown = list(df.iloc[:,1].values)
        st.write(df)
        if st.toggle('Pumping rate input in m^3/h'):
            Qs_slider = st.number_input(f'**Pumping rate (m³/h)** for the **pumping test**', 0.1,100.,10.,0.01,format="%5.2f")
            Qs = Qs_slider/3600
        else:
            Qs = st.number_input(f'**Pumping rate (m³/s)** for the **pumping test**', 0.001,0.100,0.005,0.001,format="%5.3f")
        r = st.number_input(f'**Distance** (m) from the **well** for the **observation**', 1,1000,100,1)
        b = st.number_input(f'**average Aquifer thickness** (m)', 1.,200.,10.,0.01)
        Qd = Qs*60*60*24 # m^3/d

semilog = st.toggle('Switch from log-log to semi-log plot')
# Parameter for the measured data plot

t_max = len(m_time)
d = [0 for x in range(t_max)]

fig = plt.figure(figsize=(9,6))
ax = fig.add_subplot(1, 1, 1)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)  # adjust plot area
ax.plot(m_time, m_ddown,'ro', markersize=6)
if semilog:
    plt.xscale("log")
else:
    plt.xscale("log")
    plt.yscale("log")
plt.axis([0.1,1E4,1E-2,1E+1])
ax.set(xlabel='time t (min)', ylabel='drawdown s (m)',
       title='Measured data')
ax.grid(which="both", color='grey',linewidth=0.5)

st.pyplot(fig)

# Safe the figure
# Convert figure to a BytesIO object
img_buffer = io.BytesIO()
fig.savefig(img_buffer, transparent='true', format="png", dpi=300)
img_buffer.seek(0)  # Reset buffer position

columns6 = st.columns((1,1,1), gap = 'large')
with columns6[1]:
    # Add download button
    st.download_button(
        label=":green[**Download**] **Measured-Data Graph**",
        data=img_buffer,
        file_name="measured_data_Theis.png",
        mime="image/png"
        )
        
st.subheader(':red[Type-curve matching and computation of transmissivity $T$ and storativity $S$]')        
st.markdown('''
            This section provides **step-by-step instructions describing how to perform a manual curve match**. Further, after reading the match-point vlaues from your curve match, you can use the application to compute the **transmissivity $T$** and the **storativity $S$**.
            '''
)
with st.expander(':green[**Click here**] for detailed **step-by-step instructions** about how to perform the manual Theis type-curve matching'):
    to_do(
        [(st.write, "Save the Theis type-curve on your local computer using the **Download Theis Type Curve button**. You can start with the provided match point at 1/$u$ = 1 and $W(u)$ = 1.")],"td01",)
    to_do(
        [(st.write, "Next, either load your own field-measured, drawdown-versus-time data (or use the provided ideal data). Then save an image of the measured-data graph on your local computer using the **Download Measured-Data Graph button**.")],"td02",)
    to_do(
        [(st.write, "On your local computer open software that can display pictures, for example a word processor. Then **load the saved figures (Theis Type-Curve and Measured-Data Graph) in your word processor**.")],"td03",)
    to_do(
        [(st.write, "**Allow the figure with the Measured-Data Graph to be placed _in front of the text_ such that it overlays the Theis Type-Curve**. The background of the Measured-Data Curve is transparent. Accordingly, you will be able to see the Theis type-curve through the measured data")],"td04",)
    to_do(
        [(st.write, "**Move the plot with the measured data such that the dots coincide with the type curve**.")],"td05",)
    to_do(
        [(st.write, "**Read the value of time $t_0$ (in minutes) and the drawdown $s_0$ (in meters) from the measured-data graph axes that correspond to the matching point of the Theis type-curve plot**. The green lines in the Theis type-curve will help you to find the time and drawdown values")],"td06",)
    to_do(
        [(st.write, "Finally, **compute the transmissivity $T$ and the storativity $S$ using the application by putting the values of time and drawdown in the input section below**.")],"td07",)
st.markdown('''
            After selecting the **match point** on the Theis type curve, the corresponding **time** $t_0$ and **drawdown** $s_0$ from the measured data are determined. Using these values, the **transmissivity $T$ and storativity $S$** of the aquifer can be calclated as follows:
            ''')
st.latex(r'''T = \frac{Q}{4\pi s_0 W(u)}''')

st.latex(r'''S = \frac{u T t_0}{r^2}''')
            
st.markdown('''            
            where:
            - $Q$ is the pumping rate (m³/s)
            - $s_0$ is the measured drawdown at the matching point (m)
            - $W(u)$ is the well function value at the matching point
            - $u$ is the dimensionless time parameter
            - $t_0$ is the corresponding measured time (s)
            - $r$ is the radial distance from the well (m)
            
            By aligning the measured data with the selected **match point** on the Theis type curve, these equations allow for estimation of key aquifer properties, enabling a better understanding of groundwater flow dynamics.
            ''')   
        

time_input = st.number_input('Time (min) from the type curve plot', 0.,1000., 1., 0.1)
ddown = st.number_input('Drawdown (m) from the type curve plot', 0.,1000., 1., 0.1)
time = time_input*60

transmissivity = Qs/4/np.pi/ddown*match_wu
storativity = 4*transmissivity*(time/r/r)/match_u_inv

if st.button('Show the computed results'):
    st.write("- Transmissivity **$T$ = % 10.2E"% transmissivity, " m²/s**")
    st.write("- Storativity **$S$ = % 10.2E"% storativity, "[dimensionless]**")

# TODO - INSTRUCTION HOW TO USE (MAYBE SCREENCAST)

with st.expander(':green[**Click here**] to see a **video tutorial** of the manual Theis type-curve matching'):
    st.write('Video here')
    st.video('https://youtu.be/rDqX-lgf5EA')
    
    
with st.expander(':green[**Click here**] to see an **example result** of the manual Theis type-curve matching'):
    st.markdown(""" 
        The following example shows one curve match to the ideal drawdown data 120 m from a well pumping 0.005 m³/s. The **time $t_0$** is 0.22 minutes and the **drawdown $s_0$** is 0.59 m. Therewith, the
        - transmissivity $T$ is 6.74E-04 m2/s and the 
        - storativity $S$ is 2.47E-06 (dimensionless).
        
        If many expert hydrogeologists matched a Theis curve to the data, they would all have a slightly different values of $T$ and $S$, but the parameter sets would likely all be close enough to the values of the aquifer $T$ and $S$ to draw comparable conclusions, and make similar predictions of drawdown for other distances from the well and for longer time than the duration of the test. While adjusting parameter values, one finds that the ideal data can be matched very well to the Theis curve. The reason for this behavior is that the ideal aquifer data conform to the conditions for applying the Theis solution. 
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('05_Applied_hydrogeology/FIGS/theis_manual_example.png', caption="One acceptable manual match of the Theis curve to the drawdown data")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')
# Loading the required Python libraries
import streamlit as st
from streamlit_extras.stodo import to_do
import json
from streamlit_book import multiple_choice

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Navneet Sinha": [1],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)


def render_assessment(filename, title="📋 Assessment", max_questions=4):

    with open(filename, "r", encoding="utf-8") as f:
        questions = json.load(f)

    st.markdown(f"#### {title}")
    for idx in range(0, min(len(questions), max_questions), 2):
        col1, col2 = st.columns(2)
        for col, i in zip((col1, col2), (idx, idx+1)):
            if i < len(questions):
                with col:
                    q = questions[i]
                    st.markdown(f"**Q{i+1}. {q['question']}**")
                    multiple_choice(
                        question=" ",
                        options_dict=q["options"],
                        success=q.get("success", "✅ Correct."),
                        error=q.get("error", "❌ Not quite.")
                    )


st.title('Tutorial – Numerical computation of solute transport: Demonstration of MT3D applications')

st.header('2D solute transport in a uniform groundwater flow field using :green[MODFLOW-2005, MT3D, and MODELMUSE]')

st.subheader('Overview and orientation', divider="green")

st.markdown(""" The **aim of the tutorial** is to provide an applied introduction in solute transport modeling with MODFLOW and MT3D. The applications consider two typical scenarios for an idealized groundwater catchment:
\n**:red[Scenario A]: Prediction of a :red[contamination from a continuous releasing source]** and
\n**:green[Scenario B]: Computation of a :green[solute pulse from a point source], and traveling of the solutes through the system**.
""")

lc0, rc0 = st.columns((1,1))
with lc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport.png', caption=":red[**Scenario A:**] The idealized situation for continous solute input.")
with rc0:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_tracer.png', caption=":green[**Scenario B:**]The idealized situation for a tracer test.")
st.markdown("""
Both scenarios are idealized in such a way that solute transport can be also computed with analytical solutions. This approach allows the user to understand the system, and to compare the results from the numerical model with the ‘precise’ analytical solution. Accordingly, the user gets a proper understanding of the benefits and limitations of the different methods. The scenarios and models are subsequently described.

**This app contains** materials, explanations, descriptions (as To-Do list), and videos on how to setup a MODFLOW/MT3D model for a 2D idealized catchment (see the following figure). The individual steps of the modeling process are provided in the following boxes that you can expand by clicking.
            
#### 📦 Resources used for the tutorial
The following files are provided for use throughout the tutorial...
""")

with st.expander('**... click here to see and access the ressources**'):
    st.markdown("""You can download the ressources directly using the links below. They include MODELMUSE model files for different modeling steps and supporting spreadsheets for analysis and postprocessing
    \n- 📄 PDF file with step-by-step instructions (_link to be provided_)
    - 💻 MODELMUSE model files:
        - [coarse.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/coarse.gpt) — for steps 1–3
        - [fine.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/fine.gpt) — for step 4
        - [Dirac.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/Dirac.gpt) — for step 5
        - [Dirac_Refined.gpt](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/Dirac_Refined.gpt) — for step 6
    - 📊 Spreadsheet for postprocessing:
        - [2DTransport_Tutorial.xlsx (with data)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2DTransport_Tutorial.xlsx)
        - [2DTransport_Tutorial_empty.xlsx (empty template)](https://raw.githubusercontent.com/gw-inux/Jupyter-Notebooks/main/06_Groundwater_modeling/DATA/2D_Transport/2DTransport_Tutorial_empty.xlsx)""")

st.subheader('General description of the model', divider = "green")
st.markdown("""The question and purpoose of the model, the conceptual model, and the numerical model are described in the subsequent section.""")

with st.expander(':green[**Click here for more details of the general description of the model**]'):
    
    st.markdown("""
    #### Question/Purpose of the model
    
    **🟥 Scenario A:** The general aim is the prediction and management of a contamination plume with constant release of solutes. To simulate the spreading of a solute from a point source in a confined, homogeneous and isotropic aquifer. The solute is introduced with a constant concentration. Observations exist at 100, 300, 500, and 1000 m distances.
    
    The situation is idealized and can be compared with the results of an analytical solution (2D solute transport from a continuous source with advection and dispersion). The analytical solution allows users to investigate the effects of different settings of the numerical model, like solution scheme and discretization.
    
    **🟩 Scenario B:** The general aim of this version is to use the numerical model to simulate a tracer test to characterize the aquifer. The solute is injected with a given mass over a very short term. The injection is a point source, i.e., the tracer is inserted through a point source as a Dirac impulse (10 liters in 10 seconds, containing 1,000 g NaCl). The observation is at a distance of 30 m.
    
    ---
    
    #### Conceptual model
    
    The confined aquifer is homogeneous and isotropic and sufficiently extends in the horizontal direction. The thickness of the confined aquifer is constant. Groundwater flows in a steady and uniform flow field with a defined specific velocity *q*, based on:
    
    Hydraulic gradient: *i* = 0.005  
    Hydraulic conductivity: *K* = 0.001 m/s
    
    Equation:
    
    $$
    q = -Ki = -0.001 \\times 0.005 = 5 \\times 10^{-6} \\text{ m/s} \\; (0.432 \\text{ m/d})
    $$
    
    Solute input configurations:
    - **🟥 Scenario A:** Areal source with constant concentration; width of source is 100 m.
    - **🟩 Scenario B:** Point source with slug input. Total mass input is 1,000 g in 10 liters.
    
    ---
    
    #### Mathematical model and analytical solution
    
    The analytical solutions for both scenarios are provided in two dedicated Streamlit apps:
    
    - **🟥 Scenario A:** [transport-2d-continuous.streamlit.app](https://transport-2d-continuous.streamlit.app/)
    - **🟩 Scenario B:** [transport-2d-dirac.streamlit.app](https://transport-2d-dirac.streamlit.app/)
    
    ---
    
    #### Numerical model – flow and transport
    
    **Model characteristics:**
    - One-layer 2D domain
    - Model top at 0 m, aquifer thickness: 10 m
    - Horizontal extent: 2500 m × 1100 m
    - Initial cell size: 100 m × 100 m
    - Hydraulic conductivity *K* = 1×10⁻³ m/s
    - Specified-head boundaries on west and east edges
    
    ---
    
    **🟥 Scenario A:**
    - Temporal discretization: 1 period (steady state), duration 86,400,000 s (1,000 days)
    - Contamination source from *x* = 300 to 400 m (central row)
    - Defined concentration boundary: *c* = 1 g/m³
    - Observations at 100, 300, 500, and 1,000 m downstream
    - Purpose: Predict solute transport over 1,000 days
    
    **🟩 Scenario B:**
    - Temporal discretization: 3 periods  
      - Period 1: 1 s (steady-state)  
      - Period 2: 10 s (injection, transient)  
      - Period 3: 4,319,990 s (transport, transient)
    - Injection via WEL boundary (point source at *x* = 400 m, central row)
      - Infiltration rate: 0.001 m³/s for 10 s
      - Injection concentration: 100,000 g/m³ (i.e., 1,000 g in 10 L)
    """)
with st.expander('**Show the initial assessment** - to assess your existing knowledge'):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_general_behavior.json", title="📋 Initial assessment")


st.subheader('Step-by-step tutorials to build the model with MODELMUSE', divider = "green")
st.markdown("""In the following you will find step-by-step instructions to build the flow- and transport model with MODELMUSE. Each step comes with a screencast video that shows the individual steps, and a 'ToDo' list with the essential steps. The full description of the tutorial is provided by a PDF document [for download here](www.link.com).

---

### :red[Scenario A - continuous source]

The first four steps will cover :red[**Scenario A - continuous source of solutes**]. The numerical model results will be compared to an analytical solution for a continuous point source that is shown in the subsequent figure.

💥 Try the [Streamlit App for 2D Transport with a continuous source here](https://transport-2d-continuous.streamlit.app/).""")

lc1, cc1, rc1 = st.columns((1,10,1))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport_continuous.png', caption="The synthetic catchment for the numerical model.")

# This are the links to the tutorial videos
videourl1 = 'https://youtu.be/nurSikcY4LQ'
videourl2 = 'https://youtu.be/D7a0goqD66c'
videourl3 = 'https://youtu.be/GXLGnDr0Jf0'
videourl3b = 'https://youtu.be/Opl3YpbiX-g'
videourl4 = 'https://youtu.be/NQHGZfaThXs'
videourl4b = 'https://youtu.be/U13EwH-cubY'
videourl5 = 'https://youtu.be/gNfuM5iWFMs'
videourl6 = 'https://youtu.be/tQXZmCfXEd8'

# Create ToDos to proceed with the steps of the exercise

# STEP 1
st.markdown("""
#### :red[STEP 1:] Setting up the flow model.
**Aim:** Design an idealized flow model for the confined aquifer resulting in defined uniform flow.
""")
with st.expander('🧠 **Show the initial assessment to prepare for STEP 1** - to assess your existing knowledge'):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step1.json", title="📋 Step 1 – Initial assessment")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 1**]"):
    st.markdown("""  
    This step walks you through the complete setup of a confined aquifer model using **ModelMuse** and prepares it for **particle tracking** with MODPATH.
    
    #### Directory Setup (Recommended)

    Organize your simulation files by creating separate folders:
    ```
    /Coarse/ - coarse_FD/
             - coarse_MOC/
    /Fine/   - fine_FD/
             - fine_MOC/
    ```
    This helps in comparing different solver methods and grid resolutions.
    
    #### Initial model design
    """)
#    st.markdown("#### 1. Launch and Configure ModelMuse")
#    to_do([
#        (st.write, "Open **ModelMuse**."),
#        (st.write, "Select **Create New MODFLOW Model**, then click **Next**."),
#        (st.write, "Keep default units (meters, seconds). Under description, type `2D Transport Model`. Click **Next**."),
#    ], "td001")

    to_do(
        [(st.write, "1. Launch and Configure ModelMuse."
        ,"\n - Open **ModelMuse**."
        ,"\n - Select **Create New MODFLOW Model**, then click **Next**."
        ,"\n - Keep default units (meters, seconds). Under description, type `2D Transport Model`. Click **Next**.")],"td001",)

    to_do(
        [(st.write, "2. Model selection and initial grid definition"
        ,"\n - Select 'MODFLOW version: MODFLOW-2005'"
        ,"\n - Columns: 25 (Width = 100), Rows: 11 (Width = 100), Layers: 1."
        ,"\n - Model Top = 0, Aquifer Base = -10"
        ,"\n - Click **Finish** to generate the grid.")],"td002",)
        
    to_do(
        [(st.write, "3. Time and Solver Settings."
        ,"\n - Go to **Model > MODFLOW Time**:"
        ,"\n - Starting Time: `0`, Ending Time: `86400000`"
        ,"\n - Max First Time Step Length: `86400000` → Click **OK**.")], "td003")

    to_do(
        [(st.write, "4. Activate Packages and Set K"
        ,"\n - Go to **Model > MODFLOW Packages and Programs**."
        ,"\n - Enable **Specified Head (CHD)** under Boundary Conditions → Click **OK**."
        ,"\n - Go to **Data > Edit Data Sets > Required > Hydrology**, set `Kx = 0.001` → Apply and Close.")], "td004")

    to_do(
        [(st.write, "5. Boundary Conditions"
        ,"\n - **Left boundary:** Use line tool to create vertical line on left edge, name it `left_CHD`."
        ,"\n - Go to MODFLOW Features > CHD → Set Start/End Time: `0` to `86400000`, Head: `22` → OK."
        ,"\n - **Right boundary:** Same process, name `right_CHD`."
        ,"\n - Set Start/End Head to `10`. MODFLOW Features > CHD → OK.")], "td005")

    st.markdown("#### ⚠️ Note on Warnings")
    st.info("ModelMuse might show a **georeferencing warning**. You can safely ignore this if you're working with conceptual models.")
    
    st.markdown("""
    #### Running the model and postprocessing of results
    """)
    
    to_do(
        [(st.write, "6. Run MODFLOW"
        ,"\n - Click green triangle to run MODFLOW."
        ,"\n - Save as `coarse.nam` in the appropriate folder."
        ,"\n - Verify results via ModelMonitor (green smiley = success), then review listing file.")], "td006")

    to_do(
        [(st.write, "7. Configure MODPATH"
        ,"\n - Go to **Model > MODFLOW Packages and Programs > Post Processors**."
        ,"\n - Enable **MODPATH**. Set Version: 6, Output Mode: Pathlines, Direction: Forward."
        ,"\n - Under Version Options: `StopOption = Stop at termination points (Steady State)`.")], "td007")

    to_do(
        [(st.write, "8. Place Particles"
        ,"\n - Select object tool, double-click `left_CHD`."
        ,"\n - Go to MODFLOW Features > MODPATH, choose `Grid` placement → OK.")], "td008")

    to_do(
        [(st.write, "9. Output + Final Run"
        ,"\n - Go to **MODFLOW Output Control > Head**, set to **Binary**."
        ,"\n - Save model (Ctrl+S), then click triangle to re-run."
        ,"\n - Ignore MODPATH v7 warning if prompted — we use v6.")], "td009")

    to_do(
        [(st.write, "10. Visualize Pathlines"
        ,"\n - Click **Data Visualization > MODPATH Pathlines**."
        ,"\n - Load the `.path` file → Apply → Close.")], "td010")

    st.markdown("""#### Video tutorial for Step 1
    The video shows all steps as a screencast. 
    """)

    st.video(videourl1)
    
    st.markdown("""
    #### Conclusion:
    The flow model is defined. Particle tracking enables the verification of flow. With the listing file, we can understand the model and analyze/quantify the flows. This step covered all steps in the model design for a numerical flow model.
    
    You've now created and simulated a simple MODFLOW-2005 flow model with defined head boundaries (CHD package) and particle tracking using MODPATH. This uniform flow model forms the foundation for the subsequent solute transport analysis.
    """)
 
with st.expander('**📋 Final assessment – Review what you learned in Step 1**'):
    render_assessment(
        filename="06_Groundwater_modeling/QUESTIONS/final_2D_trans_step1.json",
        title="📋 Final assessment",
        max_questions=6
    )
 
# STEP 2
st.markdown("""
#### :red[STEP 2:] Setting up the transport model with the FD scheme
**Aim:** Setting up the transport model with the FD scheme: Performing an initial solute transport simulation. Running the FD method. Postprocessing the results and analyzing the simulation.
""")  

with st.expander("🧠 **Initial Assessment – Step 2**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step2.json", "Initial Assessment for Step 2")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 2**]"):
    st.markdown("""
    More about step2
    """)
    to_do(
        [(st.write, "...")],"td04",)
    to_do(
        [(st.write, "...")],"td05",)
    to_do(
        [(st.write, "...")],"td06",)
    to_do(
        [(st.write, "...")],"td07",)

    st.markdown("""
    #### Video tutorial of step 2
    The video shows all steps as a screencast. 
    """)
    st.video(videourl2)    
 
    st.markdown("""
    #### Conclusions:
    The computed concentrations and breakthrough curves look reasonable. The mass balance is considered as plausible with minimum discrepancy. The runtime of the numerical transport model can be quantified.
    """)

with st.expander("📋 **Final Assessment – Step 2**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step2.json", "Final Assessment for Step 2", max_questions=6)
    
# STEP 3
st.markdown("""
#### :red[STEP 3:] Running the transport simulation with the MOC scheme
**Aim:** Changing the solution algorithm to the MOC scheme: Performing an solute transport simulation with MOC. Optimizing the MOC method. Postprocessing the results and analyzing the simulation.
""")  

with st.expander("🧠 **Initial Assessment – Step 3**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step3.json", "Initial Assessment for Step 3")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 3**]"):
    st.markdown("""
    More about step 3
    """)
    to_do(
        [(st.write, "...")],"td08",)
        
    to_do(
        [(st.write, "...")],"td09",)
        
    to_do(
        [(st.write, "...")],"td10",)
        
    to_do(
        [(st.write, "...")],"td11",)
        
    to_do(
        [(st.write, "...")],"td12",)
    
    st.markdown(""" 
    #### Substep 2
    """)
    to_do(
        [(st.write, "...")],"td13",)
        
    to_do(
        [(st.write, "...")],"td14",)
        
    to_do(
        [(st.write, "...")],"td15",)

    to_do(
        [(st.write, "select “Create rectangle object” for recharge zone containing outflow boundary."
        ,"\n - Click on the upper right corner of the grid in the top view with the left mouse button; press the left mouse button again, keep it down, move the cursor to (2000, 0), and release the left mouse button."
        ,"\n - name object (like “recharge_right”)."
        ,"\n - select “MODFLOW Features” and “RCH”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Recharge rate,” type the following expression into the input field: 200/1000/365.25/86400, press “OK,” and press “OK” again.")],"td16",)    
    
    st.markdown(""" 
    #### Substep 3
    """)
        
    to_do(
        [(st.write, "...")],"td17",)
        
    to_do(
        [(st.write, "...")],"td18",)
        
    to_do(
        [(st.write, "select “Create polyline object” (symbol consisting of three line segments, two rows below “View”) for river."
        ,"\n - Click on the lower-left corner in the top view with the left mouse button, move the cursor to (2500, 1500), and double-click."
        ,"\n - name polyline object (like “river”)."
        ,"\n - select “MODFLOW Features” and “RIV”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “River stage,” type the following expression into the input field: interpolate (x, 260, 0, 258, 2500), and press “OK.”."
        ,"\n - select “F()” below “Conductance per unit length or area,” type the following expression into the input field: 1000/86400, and press “OK” (This corresponds to a streambed conductance of 1000 m²/d.)."
        ,"\n - select “F()” below “River bottom,” type the following expression into the input field: interpolate (x, 255, 0, 253, 2500), press “OK,” and press “OK” again (This corresponds to a water depth of 5 m.).")],"td19",)
        
    st.markdown(""" 
    #### Substep 4
    """)
        
    to_do(
        [(st.write, "...")],"td20",)
        
    to_do(
        [(st.write, "...")],"td21",)
        
    to_do(
        [(st.write, "...")],"td22",)
        
    to_do(
        [(st.write, "select “Create point object” for the second well ."
        ,"\n - Click on the cell containing the well location (3050, 1450)."
        ,"\n - name point object (like “well 2”)."
        ,"\n - select “MODFLOW Features” and “WEL”."
        ,"\n - set starting time = -1 and ending time = 0."
        ,"\n - select “F()” below “Pumping rate per unit length or area”, type the following expression into the in-put field: -5000/86400, and press “OK” (Please do not forget the negative sign! Input corresponds to a pumping rate of 5000 m³/d.).")],"td23",)        

    st.markdown("""
    #### Video tutorial of step 3
    
    The first video tutorial demonstrate the model design for the 2D solute transport computation with MOC.
    """)
    
    st.video(videourl3)
    
    st.markdown(""" 
    The second video tutorial demonstrate some advanced post processing of the numerical solute transport model.
    """)
    
    st.video(videourl3b)

with st.expander("📋 **Final Assessment – Step 3**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step3.json", "Final Assessment for Step 3", max_questions=6)
# STEP 4

st.markdown("""
#### :red[STEP 4:] Refining the grid size and re-running the FD and MOC simulations.
**Aim:** Adapting the spatial discretization. Running the simulation with FD and MOC. Understand the effect of the grid size on the results of the computation. Postprocessing the results and analyzing the simulation.
""")  

with st.expander("🧠 **Initial Assessment – Step 4**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step4.json", "Initial Assessment for Step 4")

with st.expander("🛠️ :red[**Expand to see the instructions and screencast video for STEP 4**]"):
    st.markdown("""
    More about step 4
    """)
    to_do(
        [(st.write, "select “Data” / “Edit Data Sets” / “Required” in the menu bar.")],"td24",)
        
    to_do(
        [(st.write, "select “Modflow_Initial_Head”, then set initial head = 257, press “Apply” and press “Close” .")],"td25",)
    
    st.markdown(""" 
            #### Run Simulation / MODFLOW
           """)    
        
    to_do(
        [(st.write, "select “File” / “Save” (no model archive needs to be created) .")],"td26",)
        
    to_do(
        [(st.write, "select “Run MODFLOW-2005” by clicking on the green triangle below “Grid”.")],"td27",)
        
    to_do(
        [(st.write, "confirm the file name to save MODFLOW input files (*.nam where “*” stands for the model name).")],"td28",)
        
    to_do(
        [(st.write, "check information from ModelMonitor (“green smileys” – hopefully …).")],"td29",)
        
    to_do(
        [(st.write, "close ModelMonitor window .")],"td30",)
        
    st.markdown("""
    #### Video tutorial of step 4
    
    The first video tutorial demonstrate the model design and the computation for FD and MOC.
    """)
    
    st.video(videourl4)    
    
    st.markdown(""" 
    The second video tutorial demonstrate some advanced post processing of the numerical solute transport model.
    """)
    st.video(videourl4b)  

with st.expander("📋 **Final Assessment – Step 4**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step4.json", "Final Assessment for Step 4", max_questions=6)
    
st.markdown("""
---
### :green[Scenario B - pulse injection (Dirac)]

The following two steps will cover :green[**Scenario B - pulse injection (tracer test)**]. The numerical model results will be compared to an analytical solution for a continuous point source that is shown in the subsequent figure.

💥 Try the [Streamlit App for 2D Transport for a Dirac injection pulse here](https://transport-2d-dirac.streamlit.app/).""")

lc1, cc1, rc1 = st.columns((1,10,1))
with cc1:
    st.image('06_Groundwater_modeling/FIGS/2D_idealized_transport_pulse.png', caption="The synthetic catchment for the numerical model.")

    
    
# STEP 5
st.markdown("""
#### :green[STEP 5:] Adapting the existing model to simulate a tracer test - solute input as Dirac pulse. Running the FD and MOC simulations.
**Aim:** Adapt an model to reflect a different scenario. Implement an injection well for the Dirac pulse scenario. 
""")  

with st.expander("🧠 **Initial Assessment – Step 5**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step5.json", "Initial Assessment for Step 5")

with st.expander("🛠️ :green[**Expand to see the instructions and screencast video for STEP 5**]"):
    st.markdown("""
    More about step 5
    """)
    to_do(
        [(st.write, "...")],"td031",)

    to_do(
        [(st.write, "...")],"td032",)
        
    st.markdown("""
    #### Video tutorial of step 5
    """)
            
    st.video(videourl5)

with st.expander("📋 **Final Assessment – Step 5**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step5.json", "Final Assessment for Step 5", max_questions=6)
    
# STEP 6
st.markdown("""
#### :green[STEP 6:] Refining the existing model for the tracer test and re-running the FD and MOC simulations.
**Aim:** Understand the effect of the spatial discretization. Adapt the Dirac pulse model and evaluate the performance and accuracy by comparing the results with an analytical solution. 
""")  

with st.expander("🧠 **Initial Assessment – Step 6**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/initial_2D_trans_step6.json", "Initial Assessment for Step 6")

with st.expander("🛠️ :green[**Expand to see the instructions and screencast video for STEP 6**]"):
    st.markdown("""
    More about step 6
    """)
    to_do(
        [(st.write, "...")],"td033",)

    to_do(
        [(st.write, "...")],"td034",)
        
    st.markdown("""
    #### Video tutorial of step 6
    """)
            
    st.video(videourl6)

with st.expander("📋 **Final Assessment – Step 6**"):
    render_assessment("06_Groundwater_modeling/QUESTIONS/final_2D_trans_step6.json", "Final Assessment for Step 6", max_questions=6)
  
# OPTIONALLY STEPS
    
# STEP 6
st.markdown("""
---
#### :rainbow[OPTIONALLY STEPs:] Some further things to do.
**Aim:** Starting with own investigations. Extending the existing modles and solutions. 
""")  
with st.expander(":rainbow[**Expand to see the instructions**]"):
    st.markdown("""
            #### Optionally STEPs: Further Investigations
            
            These steps are designed to expand your modeling skills and deepen your understanding of solute transport processes, numerical methods, and model performance. They complement the main tutorial and offer opportunities for independent exploration.
            
            **1. Compare alternative numerical solution methods**
            **Aim:** Explore the differences between available advection schemes in MT3D and understand their effects on model behavior.
            - Switch between FD, MOC, TVD, MMOC, and HMOC schemes in the ADV package.
            - Compare plume shapes, breakthrough curves (with the spreadsheet and the analytical solution), and mass balance errors.
            - Evaluate numerical dispersion and runtime across methods.
            
            **2. Introduce heterogeneity in hydraulic conductivity**
            **Aim:** Investigate how spatial heterogeneity influences flow paths and solute transport.
            - Create zones or layers with varying hydraulic conductivity.
            - Implement block-wise structures or similar.
            - Visualize plume deformation and preferential pathways; also by using MODPATH.
            - Compare with results from a homogeneous setup.
            
            **3. Evaluate model performance under varying grid resolutions**
            **Aim:** Quantify the effect of discretization on numerical dispersion and computational cost.
            - Test multiple cell sizes (e.g., 100 m → 10 m → 2 m).
            - Monitor Peclet number and mass balance errors.
            - Use the analytical solution to quantify numerical error.
            - Plot error vs. cell size for FD and MOC.
            
            **4. Implement vertical layering (pseudo-3D)**
            **Aim:** Simulate simplified vertical transport and understand layer interactions.
            - Add a second or third model layer.
            - Vary vertical conductivity and dispersion.
            - Simulate upward or downward leakage.
            - Assess if the added complexity improves realism.
            
            **5. Design and interpret synthetic monitoring networks**
            **Aim:** Improve skills in selecting and interpreting monitoring locations.
            - Place observation wells at strategic distances and angles.
            - Analyze breakthrough curves and concentration time series.
            - Evaluate the representativeness of monitoring data relative to the full plume.
           """)     
           
st.markdown('---')

# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('90_Streamlit_apps/GWP_Boundary_Conditions/assets/images/CC_BY-SA_icon.png')
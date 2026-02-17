Weda.io-A Climate Prediction & Crop Advisory App
Overview
Weda.io is a climate prediction and crop advisory application built with African farmers and agricultural investors in mind.
Extreme weather events continue to cause severe agricultural losses across Africa. For example, the Food and Agriculture Organization (FAO) documented approximately ₦4 trillion worth of food loss in Benue State in 2024 due to flooding in major agricultural hubs. Climate variability has increasingly made agricultural investment unpredictable.
Weda.io aims to reduce that uncertainty.
  - This pilot project uses historical climate data to:
  - Predict total precipitation over a selected period
  - Predict average temperature over a selected period
  - Assess crop–climate compatibility-Provide actionable advisory insights for crop planning

Problem Statement
Agricultural investment in many African regions is highly vulnerable to:
  - Flooding
  - Irregular rainfall patterns
  - Temperature shifts
  - Climate change–driven variability
Farmers and investors often operate without localized predictive tools tailored to their specific agro-ecological conditions.

What Weda.io Does
This pilot implementation is built using Climate Data Store (CDS) data collected in: Mokwa, Niger State, Nigeria
Climate Prediction
Rainfall Prediction
  - Model: SARIMA
  - Mean Absolute Error (MAE): 24.13

Temperature Prediction
  - Model: AutoETS
  - Mean Absolute Error (MAE): 0.498

Users select a forecast period, and the system generates predicted:
  - Total precipitation
  - Average temperature
  - Crop Compatibility Engine

After generating predictions, the system:
  - Evaluates the climate conditions
  - Compares them to crop suitability thresholds
  - Produces a structured advisory message on crop viability

Demo
You can explore the project here:
🔗 https://weda-predict.streamlit.app/

Model Details
Rainfall Model
Type: Seasonal ARIMA (SARIMA)
Seasonal length: 12
Performance metric: MAE = 24.13
Currently under optimization. Further experimentation is ongoing to improve rainfall prediction accuracy and robustness.

Temperature Model
Type: AutoETS
Seasonal length: 12
Performance metric: MAE = 0.498

Target Users
  - Farmers
  - Agricultural investors
  - Government planning bodies
  - Climate and food system researchers

Impact Goals
Weda.io aims to:
  - Strengthen food system resilience
  - Mitigate climate-related agricultural risks
  - Improve crop planning decisions
  - Enhance economic productivity in Africa’s agricultural sector

Current Limitations
This is a pilot study based on data from one region (Mokwa, Niger State). The rainfall model is still undergoing refinement. Generalizability across different African agro-ecological zones is currently limited. 
Real-time deployment features are under development.

Future Improvements
  - Expand dataset coverage across multiple African regions
- Integrate satellite and remote sensing data
- Improve rainfall model accuracy
- Develop a web/mobile interface
- Add multi-crop suitability scoring

Contributions
This project is still evolving. Contributions, feedback, and collaboration are welcome.




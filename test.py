import pandas as pd
from utils.sarima import run_forecast, temp_forecast, get_crop_data, interpret_with_llm, plot_result

crop_df = pd.read_csv('C:/Users/LENOVO/Documents/python_data_analytics_course/Pod 2 Project/Makwa crop data - Sheet4.csv')
df = pd.read_csv('C:/Users/LENOVO/Documents/python_data_analytics_course/Pod 2 Project/sarima_app/utils/data/Temperature/era_5_2000_2026.csv')
rain_df = pd.read_csv('C:/Users/LENOVO/Documents/python_data_analytics_course/Pod 2 Project/sarima_app/utils/data/rainfall_2000_2026.csv')

#rain = run_forecast(rain_df, 3)
temp = temp_forecast(df, 3)

#result = plot_result(rain, temp, 3)

print(temp)


 
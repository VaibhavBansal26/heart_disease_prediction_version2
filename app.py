import streamlit as st
import json
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd 


st.title('Heart Disease Prediction App')

# Define the numerical and categorical columns
numerical_columns = [
    'Age', 'BloodPressure', 'Cholesterol', 'MaxHeartRate', 'Peak'
]
categorical_columns = [
    'Sex', 'ChestPain', 'FastingBloodSugar', 'ECG', 'Angina', 'Slope', 'Flourosopy', 'ReversableDefect',
    'AgeCategory', 'Smoker', 'TreatmentType'
]

# Load options for sidebars
with open('input_options.json') as f:
    side_bar_options = json.load(f)
    options = {}
    for key, value in side_bar_options.items():
        if key in categorical_columns:
            options[key] = st.sidebar.selectbox(key, value)
        elif key in numerical_columns:
            min_val, max_val = map(int, value)  # Ensure min_val and max_val are integers
            current_value = (min_val + max_val) // 2  # Use integer division for current_value
            options[key] = st.sidebar.slider(key, min_val, max_val, int(current_value))

# Display the options selected by the user
# st.write(options)

emoji_dict = {
    'age': '🔢', 'trestbps': '📏', 'chol': '🍔', 'thalach': '💓', 'oldpeak': '⛰️',
    'sex': '🚹🚺', 'cp': '❤️', 'fbs': '🍬', 'restecg': '📈', 'exang': '🚫', 'slope': '⛷️', 'ca': '🔢', 'thal': '🧬',
    'Age Category': '🧓', 'Smoker': '🚬', 'Treatment Type': '🔧'
}

# Transform options for display with emojis
options_for_display = [(key, f"{emoji_dict.get(key, '')} {value}") for key, value in options.items()]
options_df = pd.DataFrame(options_for_display, columns=['Predictors', 'Selections'])
options_df.reset_index(drop=True, inplace=True)

gb = GridOptionsBuilder.from_dataframe(options_df)
gb.configure_grid_options(domLayout='autoHeight')  # Default layout
grid_options = gb.build()

col1, col2 = st.columns(2)

with col1:
    # st.json(options)
    AgGrid(options_df, gridOptions=grid_options, fit_columns_on_grid_load=True)


    
prediction = None
# Prediction button
if st.button('Predict'):
    try:
        # Convert options to JSON and send to prediction server
        payload = json.dumps({'inputs': options})
        response = requests.post(
            url="http://104.236.76.123:5001/invocations",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()  # Raises an exception for HTTP errors
        prediction = response.json().get('predictions')[0]
        st.write(f'Heart disease prediction status: {prediction}')
    except requests.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

with col2:
    if prediction == 1:
        st.image('defective_heart.svg', caption='Heart Illustration')
        st.warning("Warning: Health Disease Predicted")
    else:
        st.image('heart.svg', caption='Heart Illustration')
        if prediction == 0:
            st.success("Congratulations! Healthy Heart Detected")
           

import streamlit as st
import json
import requests


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



col1, col2 = st.columns(2)

with col1:
    st.table(options)


    
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
           

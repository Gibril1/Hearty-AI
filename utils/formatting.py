def convert_data(data):
    converted_data = {}
    converted_data['Age'] = int(data.patient_report['age'])
    converted_data['Sex'] = 'Male' if data.patient_report['sex'] == '1' else 'Female'
    converted_data['Chest Pain Type'] = {
        '0': 'Typical Angina',
        '1': 'Atypical Angina',
        '2': 'Non-anginal Pain',
        '3': 'Asymptomatic'
    }[data.patient_report['cp']]
    converted_data['Resting Blood Pressure'] = int(data.patient_report['trestbps'])
    converted_data['Cholesterol'] = int(data.patient_report['chol'])
    converted_data['Fasting Blood Sugar'] = 'True' if data.patient_report['fbs'] == '1' else 'False'
    converted_data['Resting Electrocardiographic Results'] = {
        '0': 'Normal',
        '1': 'ST-T Wave Abnormality',
        '2': 'Probable or Definite Left Ventricular Hypertrophy'
    }[data.patient_report['restecg']]
    converted_data['Maximum Heart Rate Achieved'] = int(data.patient_report['thalach'])
    converted_data['Exercise Induced Angina'] = 'Yes' if data.patient_report['exang'] == '1' else 'No'
    converted_data['ST Depression Induced by Exercise'] = float(data.patient_report['oldpeak'])
    converted_data['Slope of Peak Exercise ST Segment'] = {
        '1': 'Upsloping',
        '2': 'Flat',
        '3': 'Downsloping'
    }[data.patient_report['slope']]
    converted_data['Number of Major Vessels Colored by Flourosopy'] = int(data.patient_report['ca'])
    converted_data['Thallium Stress Test Results'] = {
        '0': 'Normal',
        '1': 'Fixed Defect',
        '2': 'Reversible Defect'
    }[data.patient_report['thal']]

    
    return converted_data, data.patient_report['confidence'], data.patient_report['prediction']

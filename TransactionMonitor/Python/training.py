import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder

def guid_to_int(guid):
    if isinstance(guid, str):
        guid = guid.replace('-', '').lower()
        return int(guid, 16)
    else:
        return 0
    
def normilize_state(state):
    if state == 'high_value_approval_required':
        return 1
    elif state == 'transaction_monitoring_approval_required':
        return 0.5
    else:
        return 0
    
def normilize_bool_string(state):
    if state == 't':
        return 1
    else:
        return 0

# Load data
data = pd.read_csv('account_transactions.csv')

# Drop all columns except the ones in columns_to_keep
columns_to_keep = ['_time', 'ca_balance', 'ca_currency_id', 'ca_id', 
                   'ca_is_operating_account', 'ccc_customer_id', 'da_balance', 
                   'da_bank_account_number', 'da_bank_id', 'da_currency_id', 
                   'da_is_operating_account', 'da_is_primary', 'dc_legal_type', 
                   'dc_organization', 'dc_registered_country_id', 'p_amount', 
                   'p_currency_id', 'p_description', 'p_id', 'p_ip_address', 
                   'p_kind', 'p_state', 'p_type', 't_currency_id', 't_debit_credit', 
                   't_estimated_converted_amount', 't_reference']
data = data[columns_to_keep]

# Normilize datetime column
data['_time'] = pd.to_datetime(data['_time'])
data['_year'] = data['_time'].dt.year
data['_month'] = data['_time'].dt.month
data['_day'] = data['_time'].dt.day
data['_hour'] = data['_time'].dt.hour
data['_minute'] = data['_time'].dt.minute
data['_second'] = data['_time'].dt.second
data.drop(columns=['_time'], inplace=True)

# Normalize numerical columns
numerical_columns = ['ca_balance', 'da_balance', 'p_amount', 't_estimated_converted_amount']
scaler = StandardScaler()
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# One-hot encode categorical columns
categorical_columns = ['ca_currency_id', 'da_currency_id', 'dc_registered_country_id', 
                       'p_currency_id', 'p_kind', 'p_type', 't_currency_id', 't_debit_credit']
data = pd.get_dummies(data, columns=categorical_columns)

# Convert boolean t/f columns to 1/0
bool_columns = ['ca_is_operating_account', 'da_is_operating_account', 'da_is_primary']
for column in bool_columns:
    data[column] = data[column].apply(normilize_bool_string)

# Convert GUID columns to integers
guid_columns = ['ca_id', 'ccc_customer_id', 'da_bank_id', 'p_id']
for column in guid_columns:
    data[column] = data[column].apply(guid_to_int)

# Label encode ordinal columns
ordinal_columns = ['da_bank_account_number', 'dc_organization', 
                   'p_description', 'p_ip_address', 't_reference']
label_encoders = {}
for column in ordinal_columns:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Normalize target variable
data['p_state'] = data['p_state'].apply(normilize_state)

# Save the processed data
data.to_csv('output.csv', index=False)
print("Data processing complete")

# Split data into features and target variable
x = data.drop(columns=['p_state'])
y = data['p_state']

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Choose a model (Random Forest Regression in this example)
model = RandomForestRegressor()

# Train the model
model.fit(x_train, y_train)

# Evaluate the model
y_pred = model.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

model.save('model.pkl') # Save the model
#libraries
import pandas as pd
import pandas_ta as ta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

#setting panda
# Set the display format for float numbers
pd.options.display.float_format = '{:.2f}'.format

#read raw stock data
df = pd.read_csv('TATA.csv')

#setting columns
new_column_names = ["DATE","SERIES","OPEN", "HIGH", "LOW", "PREV CLOSE","LTP","CLOSE","VWAP","52W H","52W L","VALUE","VOLUME", "NO OF TRADES"]
df.columns = new_column_names


# initial preprocess
# Drop rows with any null values
df.dropna(inplace=True)

# Remove the comma from the 'VALUE' column
df['VALUE'] = df['VALUE'].str.replace(',', '')

# Convert 'VALUE' column to float dtype
df['VALUE'] = df['VALUE'].astype(float)

# Remove the comma from the 'NO OF TRADES' column
df['NO OF TRADES'] = df['NO OF TRADES'].str.replace(',', '')

# Convert 'NO OF TRADES' column to float dtype
df['NO OF TRADES'] = df['NO OF TRADES'].astype(float)

# Remove the comma from the 'VOLUME' column
df['VOLUME'] = df['VOLUME'].str.replace(',', '')

# Convert 'NO OF TRADES' column to float dtype
df['VOLUME'] = df['VOLUME'].astype(float)

#remove series column
df.drop("SERIES",axis=1, inplace=True)

# Convert the 'Date' column to a datetime data type
df['DATE'] = pd.to_datetime(df['DATE'])

# Extract year, month, and day of the week as new features
df['Year'] = df['DATE'].dt.year
df['Month'] = df['DATE'].dt.month
df['DayOfWeek'] = df['DATE'].dt.dayofweek

# Drop the original 'Date' column
df.drop('DATE', axis=1, inplace=True)

print(df)
print(df["VOLUME"])

#calculate technical indicators

# Calculate RSI
df['rsi'] = ta.rsi(df['CLOSE'])

# Calculate Bollinger Bands
# Define the parameters for the Bollinger Bands
window = 20  # Number of periods for the moving average
std_dev = 2  # Number of standard deviations for the bands

# Calculate the rolling mean (middle band) and rolling standard deviation for the window
df['bb_middle'] = df['CLOSE'].rolling(window).mean()
df['bb_std'] = df['CLOSE'].rolling(window).std()

# Calculate the upper band and lower band
df['bb_upper'] = df['bb_middle'] + (std_dev * df['bb_std'])
df['bb_lower'] = df['bb_middle'] - (std_dev * df['bb_std'])


# Calculate the MACD
macd = ta.macd(df['CLOSE'])

#calculate SMA
# Define the window size for the SMA
window_size = 10  # Number of periods for the moving average

# Calculate the SMA
df['sma'] = df['CLOSE'].rolling(window=window_size).mean()

# Remove rows with NaN values
df.dropna(inplace=True)


print(df)
feature_names = ["Year","Month","DayOfWeek","bb_middle","bb_std","bb_upper","bb_lower","sma","rsi","OPEN", "HIGH", "LOW", "PREV CLOSE","LTP","VWAP","52W H","52W L","VALUE","VOLUME", "NO OF TRADES"]  # Replace with actual feature names
df.columns = feature_names + ['CLOSE']  # Replace 'target' with the actual target variable name

# Split the data into input features and the target variable
X = df[feature_names]
y = df['CLOSE']
# Split the data into input features and the target variable
#X = df[]  # Replace 'feature1', 'feature2', 'feature3' with actual feature names
#y = df["CLOSE"]  # Replace 'target' with the actual target variable name

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)

# Create a linear regression model and fit it to the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the target variable for the test data
y_pred = model.predict(X_test)

# Evaluate the model using mean squared error
mse = mean_squared_error(y_test, y_pred)


print("Mean Squared Error:", mse)

# Calculate the R-squared score
r2 = r2_score(y_test, y_pred)

# Print the R-squared score as a percentage
accuracy_percentage = r2 * 100
print("Accuracy Score: {:.2f}%".format(accuracy_percentage))

# Calculate the model score
model_score = model.score(X_test, y_test)

# Print the model score
print("Model Score: {:.2f}".format(model_score))

#print(df["Month"],df["DayOfWeek"])
print(df["VOLUME"])

test_f = [2022,11,1,802.46,10.49,823.43,781.48,804.46,56.35,804.95,811.90,803.05,804.80,807.50,861.15,650.20,1278339.00,1032259772.30,29759,38851]
ff = ["Year","Month","DayOfWeek","bb_middle","bb_std","bb_upper","bb_lower","sma","rsi","OPEN", "HIGH", "LOW", "PREV CLOSE","LTP","VWAP","52W H","52W L","VALUE","VOLUME", "NO OF TRADES"]  # Replace 'feature1', 'feature2', 'feature3' with actual feature names
print(len(test_f))
print(len(ff))
print(y_pred)
output = model.predict([test_f])
print(output)
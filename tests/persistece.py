import pickle

# Data to persist
data = {'name': 'John', 'age': 25, 'city': 'New York'}

db_name = '.data.pkl'

# Writing to a file
with open(db_name, 'wb') as pkl_file:
    pickle.dump(data, pkl_file)

# Reading from a file
with open(db_name, 'rb') as pkl_file:
    loaded_data = pickle.load(pkl_file)

print("Loaded Data:", loaded_data)
import numpy as np
import sklearn as s

input_data = np.array([[5.1, -2.9, 3.3],[-1.2, 7.8, -6.1],[3.9, 0.4, 2.1],[7.3, -9.9, -4.5]])

#Binarized_Data
data_binarized = preprocessing.Binarizer(threshold=2.1).transform(input_data)
print("\nBinarized data:\n", data_binarized)


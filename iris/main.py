#%% Initials imports
import pandas as pd

#%% Load the dataset and first exploratory analisys
iris = pd.read('iris.csv', names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class'])
print(iris.head())

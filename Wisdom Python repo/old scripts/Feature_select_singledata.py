from Compile_modified import Compile
from MaxMin import MaxMin
from template import template
import numpy as np
import pandas as pd
from Compile_Volley import Compile_Volley
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# # Normalize the features
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)
# filepath= '/Users/wisdomokoro/Library/CloudStorage/OneDrive-ImperialCollegeLondon/uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/my data/'
filepath_fore ='/Users/wisdomokoro/Library/CloudStorage/OneDrive-ImperialCollegeLondon/uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/Watch Sensor/Fore_20'
filepath_back ='/Users/wisdomokoro/Library/CloudStorage/OneDrive-ImperialCollegeLondon/uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/Watch Sensor/Back_20'
filepath= filepath_fore
# filenames=[f'{filepath}_W/motion.csv',f'{filepath}_K/motion.csv',f'{filepath}_F/motion.csv',f'{filepath}_A/motion.csv',f'{filepath}_F2/motion.csv']
filenames=[f'{filepath}_W/motion.csv',f'{filepath}_K/motion.csv',f'{filepath}_A/motion.csv']



AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ = Compile(filenames)
faMax, faMin, faMean, faStd, faArea, fgMax, fgMin, fgMean, fgStd, fgArea = MaxMin(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)
AllfGyro_av, AllfAccel_av, LinSpeedf, thetah_f, thetal_f, magAlow_f, magAhigh_f = template(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)

# filepath= filepath_back
# filenames=[f'{filepath}_K/motion.csv',f'{filepath}_F/motion.csv',f'{filepath}_A/motion.csv']
# AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ = Compile(filenames)
# AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ = cross_corr(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
# baMax, baMin, baMean, baStd, baArea, bgMax, bgMin, bgMean, bgStd, bgArea = MaxMin(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
# AllbGyro_av, AllbAccel_av, LinSpeedb, thetah_b, thetal_b, magAlow_b, magAhigh_b = feature_template(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
# Backhand Topspin (139 shots) Disha, Disha, Katarina, Thomas
aMaxAll= faMax
aMinAll= faMin
aMeanAll= faMean
aStdAll= faStd
aAreaAll= faArea
gMaxAll= fgMax
gMinAll= fgMin
gMeanAll= fgMean
gStdAll= fgStd
gAreaAll= fgArea

fA = np.hstack((aMaxAll, aMinAll, aMeanAll, aStdAll, aAreaAll, gMinAll, gMaxAll, gMeanAll, gStdAll, aAreaAll))

#Load the SVM model
svm = joblib.load('/Users/wisdomokoro/Library/CloudStorage/OneDrive-ImperialCollegeLondon/uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/MODELS/cross_cor_4_shot.pkl')
# Transform the data using the PCA model
scaler = StandardScaler()
fA_std = scaler.fit_transform(fA)

# Predict the class using the SVM model
fA_PCA_pred = svm.predict(fA_std)

# Calculate accuracy
n= len(fA_PCA_pred)
Forehand= [1,3,5]
Backhand= [2,4,6]
count= 0
for i in range(n):
    if fA_PCA_pred[i] == 2:
        count+=1
accuracy = count/n

print('Accuracy: ', accuracy)
print('Predicted class: ', fA_PCA_pred)

labels= ['Forehand','Backhand','Volley','Serve']

# Calculate confusion matrix
cm = confusion_matrix(y_true= np.array([1]*len(fA_PCA_pred)),y_pred= fA_PCA_pred)

# Plot confusion matrix
sns.heatmap(cm, annot=True, cmap='Blues', fmt='d',xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted Class')
plt.ylabel('True Class')
plt.title('Confusion Matrix')
plt.show()

# Calculate percentages for each class
confusion_mat_percent = cm / cm.sum(axis=1)[:, np.newaxis]

# Create a heatmap of the confusion matrix with percentages
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_mat_percent, annot=True, cmap='Blues', fmt='.2%', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Percentages)')
#%%
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
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold 

datapath= '/Users/wisdomokoro/Library/CloudStorage/OneDrive-ImperialCollegeLondon/uni/FYP-DESKTOP-27I1PBE/FYP--WIsdom/Disha Redo/Data/'
#%%
# Forehand All (126 shots)
filenames = [f'{datapath}00049_CalInertialAndMag.csv', f'{datapath}00060_CalInertialAndMag.csv', f'{datapath}00065_CalInertialAndMag.csv', f'{datapath}00068_CalInertialAndMag.csv']
AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ = Compile(filenames)
faMax, faMin, faMean, faStd, faArea, fgMax, fgMin, fgMean, fgStd, fgArea = MaxMin(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)
AllfGyro_av, AllfAccel_av, LinSpeedf, thetah_f, thetal_f, magAlow_f, magAhigh_f = template(AllfGyroX, AllfGyroY, AllfGyroZ, AllfAccelX, AllfAccelY, AllfAccelZ)
#%%
# Backhand Topspin (139 shots) Disha, Disha, Katarina, Thomas
filenames = [ f'{datapath}00050_CalInertialAndMag.csv', f'{datapath}00066_CalInertialAndMag.csv', f'{datapath}00069_CalInertialAndMag.csv']
AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ = Compile(filenames)
baMax, baMin, baMean, baStd, baArea, bgMax, bgMin, bgMean, bgStd, bgArea = MaxMin(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
AllbGyro_av, AllbAccel_av, LinSpeedb, thetah_b, thetal_b, magAlow_b, magAhigh_b = template(AllbGyroX, AllbGyroY, AllbGyroZ, AllbAccelX, AllbAccelY, AllbAccelZ)
#%%#
#Backhand Slice (58 shots) Disha, Disha, Katarina, Thomas
filenames = [ f'{datapath}00856_CalInertialAndMag.csv', f'{datapath}00857_CalInertialAndMag.csv']
AllbsGyroX, AllbsGyroY, AllbsGyroZ, AllbsAccelX, AllbsAccelY, AllbsAccelZ = Compile(filenames)     
bsaMax, bsaMin, bsaMean, bsaStd, bsaArea, bsgMax, bsgMin, bsgMean, bsgStd, bsgArea = MaxMin(AllbsGyroX, AllbsGyroY, AllbsGyroZ, AllbsAccelX, AllbsAccelY, AllbsAccelZ)
AllbsGyro_av, AllbsAccel_av, LinSpeedbs, thetah_bs, thetal_bs, magAlow_bs, magAhigh_bs = template(AllbsGyroX, AllbsGyroY, AllbsGyroZ, AllbsAccelX, AllbsAccelY, AllbsAccelZ)
#%%
# Forehand Slice (274 shots) Disha, Hannah, Katarina, thomas
filenames=[f'{datapath}00992_CalInertialAndMag.csv',f'{datapath}00991_CalInertialAndMag.csv',f'{datapath}00994_CalInertialAndMag.csv']
[AllfsGyroX,AllfsGyroY,AllfsGyroZ,AllfsAccelX,AllfsAccelY,AllfsAccelZ]=Compile(filenames)
[fsaMax,fsaMin,fsaMean,fsaStd,fsaArea,fsgMax,fsgMin,fsgMean,fsgStd,fsgArea]= MaxMin(AllfsGyroX,AllfsGyroY,AllfsGyroZ,AllfsAccelX,AllfsAccelY,AllfsAccelZ)
[AllfsGyro_av, AllfsAccel_av, LinSpeedfs,thetah_fs,thetal_fs,magAlow_fs,magAhigh_fs] = template(AllfsGyroX,AllfsGyroY,AllfsGyroZ,AllfsAccelX,AllfsAccelY,AllfsAccelZ)

# Volley Backhand (58 shots)
filenames = [f'{datapath}00859_CalInertialAndMag.csv', f'{datapath}00862_CalInertialAndMag.csv']
AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ = Compile(filenames)
vbaMax, vbaMin, vbaMean, vbaStd, vbaArea, vbgMax, vbgMin, vbgMean, vbgStd, vbgArea = MaxMin(AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ)
AllvbGyro_av, AllvbAccel_av, LinSpeedvb, thetah_vb, thetal_vb, magAlow_vb, magAhigh_vb = template(AllvbGyroX, AllvbGyroY, AllvbGyroZ, AllvbAccelX, AllvbAccelY, AllvbAccelZ)
# Volley Forehand (57 shots)
filenames = [f'{datapath}00858_CalInertialAndMag.csv', f'{datapath}00860_CalInertialAndMag.csv']
AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ = Compile(filenames)
vfaMax, vfaMin, vfaMean, vfaStd, vfaArea, vfgMax, vfgMin, vfgMean, vfgStd, vfgArea = MaxMin(AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ)
AllvfGyro_av, AllvfAccel_av, LinSpeedvf, thetah_vf, thetal_vf, magAlow_vf, magAhigh_vf = template(AllvfGyroX, AllvfGyroY, AllvfGyroZ, AllvfAccelX, AllvfAccelY, AllvfAccelZ)
# Serve All (66 shots)
filenames = [f'{datapath}00057_CalInertialAndMag.csv', f'{datapath}00067_CalInertialAndMag.csv', f'{datapath}00070_CalInertialAndMag.csv']
AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ = Compile(filenames)
saMax, saMin, saMean, saStd, saArea, sgMax, sgMin, sgMean, sgStd, sgArea = MaxMin(AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ)
AllsGyro_av, AllsAccel_av, LinSpeeds, thetah_s, thetal_s, magAlow_s, magAhigh_s = template(AllsGyroX, AllsGyroY, AllsGyroZ, AllsAccelX, AllsAccelY, AllsAccelZ)

# Assuming that faMax, baMax, etc. are defined and are NumPy arrays
# Assuming that faMax, baMax, etc. are defined and are NumPy arrays
aMaxAll = np.vstack((faMax, baMax, fsaMax, bsaMax, vfaMax, vbaMax, saMax))
aMinAll = np.vstack((faMin, baMin, fsaMin, bsaMin, vfaMin, vbaMin, saMin))
aMeanAll = np.vstack((faMean, baMean, fsaMean, bsaMean, vfaMean, vbaMean, saMean))
aStdAll = np.vstack((faStd, baStd, fsaStd, bsaStd, vfaStd, vbaStd, saStd))
aAreaAll = np.vstack((faArea, baArea, fsaArea, bsaArea, vfaArea, vbaArea, saArea))
gMinAll = np.vstack((fgMin, bgMin, fsgMin, bsgMin, vfgMin, vbgMin, sgMin))
gMaxAll = np.vstack((fgMax, bgMax, fsgMax, bsgMax, vfgMax, vbgMax, sgMax))
gMeanAll = np.vstack((fgMean, bgMean, fsgMean, bsgMean, vfgMean, vbgMean, sgMean))
gStdAll = np.vstack((fgStd, bgStd, fsgStd, bsgStd, vfgStd, vbgStd, sgStd))
gAreaAll = np.vstack((fgArea, bgArea, fsgArea, bsgArea, vfgArea, vbgArea, sgArea))

# Generate table for testing trained model
# And also add a column to show which class/type of stroke it is
t_1 = np.zeros((len(aAreaAll[:,1]), 1))
shots=[]
count= 0
for i in [faMax, baMax, fsaMax, bsaMax, vfaMax, vbaMax, saMax]:
    shots += [count+len(i[:,1])]
    count+= len(i[:,1])
t_1[0:shots[0]] = 1  # forehand 126
t_1[shots[0]:shots[1]] = 2  # backhand 139
t_1[shots[1]:shots[2]] = 3  # forehand slice 274
t_1[shots[2]:shots[3]] = 4  # backhand slice 122
t_1[shots[3]:shots[4]] = 5  # volley forehand 57
t_1[shots[4]:shots[5]] = 6  # volley backhand 58
t_1[shots[5]:shots[6]] = 7  # serve 66

fA = np.hstack((aMaxAll, aMinAll, aMeanAll, aStdAll, aAreaAll, gMinAll, gMaxAll, gMeanAll, gStdAll, aAreaAll))


  # all columns except the last one

#%%
# Assuming `complete_table` is your DataFrame and 'Class' is your target column
X =fA #checkTable.drop('Class', axis=1)
y = t_1#checkTable['Class']

#%%
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Normalize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#%%
# # Apply PCA for dimensionality reduction
# pca = PCA(n_components=0.95)  # Retain 95% of the variance
# X_train_pca = pca.fit_transform(X_train)
# X_test_pca = pca.transform(X_test)

# Train the SVM model
svm_model = SVC(kernel='rbf', C=100, gamma='auto')
svm_model.fit(X_train, y_train)

#%%
# Save the trained model
joblib.dump(svm_model, 'mediumSVM_gyro_change_PCA.pkl')

# # Save the PCA object
# joblib.dump(pca, 'pca_model.pkl')

# # Load the PCA object
# pca = joblib.load('pca_model.pkl')
#%%
# Make predictions
y_pred = svm_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
#%%
# Generate confusion matrix
confusion_mat = confusion_matrix(y_test, y_pred)

# print(confusion_mat)

# Assuming `confusion_mat` is the confusion matrix obtained from your model
labels = ['Forehand', 'Backhand', 'Forehand Slice', 'Backhand Slice', 'Volley Forehand', 'Volley Backhand', 'Serve']

# Create a heatmap of the confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_mat, annot=True, cmap='Blues', fmt='d', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
# Assuming `confusion_mat` is the confusion matrix obtained from your model
labels = ['Forehand', 'Backhand', 'Forehand Slice', 'Backhand Slice', 'Volley Forehand', 'Volley Backhand', 'Serve']

# Calculate percentages for each class
confusion_mat_percent = confusion_mat / confusion_mat.sum(axis=1)[:, np.newaxis]

# Create a heatmap of the confusion matrix with percentages
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_mat_percent, annot=True, cmap='Blues', fmt='.2%', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix (Percentages)')

plt.show()
print("Accuracy is", accuracy*100, "%")


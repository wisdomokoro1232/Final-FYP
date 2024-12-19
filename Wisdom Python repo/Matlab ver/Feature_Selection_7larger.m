%% Feature selection Compiled with 7 classes
% 
clc %clears the command window
close all %close all windows
clear all %clears the workspace

%% Forehand All (126 shots)
Filename1='00049_CalInertialAndMag.csv';% Disha
Filename2='00060_CalInertialAndMag.csv';% Hannah
Filename3='00065_CalInertialAndMag.csv';% Katarina
Filename4='00068_CalInertialAndMag.csv';% Thomas
[AllfGyroX,AllfGyroY,AllfGyroZ,AllfAccelX,AllfAccelY,AllfAccelZ]=Compile(Filename1,Filename2,Filename3,Filename4);
[faMax,faMin,faMean,faStd,faArea,fgMax,fgMin,fgMean,fgStd,fgArea]= MaxMin(AllfGyroX,AllfGyroY,AllfGyroZ,AllfAccelX,AllfAccelY,AllfAccelZ);
[AllfGyro_av, AllfAccel_av, LinSpeedf,thetah_f,thetal_f,magAlow_f,magAhigh_f] = template(AllfGyroX,AllfGyroY,AllfGyroZ,AllfAccelX,AllfAccelY,AllfAccelZ);
%% Backhand Topspin (139 shots)
Filename1='00050_CalInertialAndMag.csv';% Disha
Filename2='00050_CalInertialAndMag.csv';% Disha
Filename3='00066_CalInertialAndMag.csv';% Katarina
Filename4='00069_CalInertialAndMag.csv';% Thomas
[AllbGyroX,AllbGyroY,AllbGyroZ,AllbAccelX,AllbAccelY,AllbAccelZ]=Compile(Filename1,Filename2,Filename3,Filename4);
[baMax,baMin,baMean,baStd,baArea,bgMax,bgMin,bgMean,bgStd,bgArea]= MaxMin(AllbGyroX,AllbGyroY,AllbGyroZ,AllbAccelX,AllbAccelY,AllbAccelZ);
[AllbGyro_av, AllbAccel_av,LinSpeedb,thetah_b,thetal_b,magAlow_b,magAhigh_b] = template(AllbGyroX,AllbGyroY,AllbGyroZ,AllbAccelX,AllbAccelY,AllbAccelZ);
%% Forehand Slice (274 shots)
Filename1='00992_CalInertialAndMag.csv';% Disha
Filename2='00991_CalInertialAndMag.csv';% Hannah
Filename3='00994_CalInertialAndMag.csv';% Katarina
Filename4='00992_CalInertialAndMag.csv';% Thomas
[AllfsGyroX,AllfsGyroY,AllfsGyroZ,AllfsAccelX,AllfsAccelY,AllfsAccelZ]=Compile(Filename1,Filename2,Filename3,Filename4);
[fsaMax,fsaMin,fsaMean,fsaStd,fsaArea,fsgMax,fsgMin,fsgMean,fsgStd,fsgArea]= MaxMin(AllfsGyroX,AllfsGyroY,AllfsGyroZ,AllfsAccelX,AllfsAccelY,AllfsAccelZ);
[AllfsGyro_av, AllfsAccel_av, LinSpeedfs,thetah_fs,thetal_fs,magAlow_fs,magAhigh_fs] = template(AllfsGyroX,AllfsGyroY,AllfsGyroZ,AllfsAccelX,AllfsAccelY,AllfsAccelZ);

%% Backhand Slice (122 shots)
Filename1='00856_CalInertialAndMag.csv';% Disha
Filename2='00856_CalInertialAndMag.csv';% Disha
Filename3='00857_CalInertialAndMag.csv';% Katarina
Filename4='00857_CalInertialAndMag.csv';% Thomas
[AllbsGyroX,AllbsGyroY,AllbsGyroZ,AllbsAccelX,AllbsAccelY,AllbsAccelZ]=Compile(Filename1,Filename2,Filename3,Filename4);
[bsaMax,bsaMin,bsaMean,bsaStd,bsaArea,bsgMax,bsgMin,bsgMean,bsgStd,bsgArea]= MaxMin(AllbsGyroX,AllbsGyroY,AllbsGyroZ,AllbsAccelX,AllbsAccelY,AllbsAccelZ);
[AllbsGyro_av, AllbsAccel_av,LinSpeedbs,thetah_bs,thetal_bs,magAlow_bs,magAhigh_bs] = template(AllbsGyroX,AllbsGyroY,AllbsGyroZ,AllbsAccelX,AllbsAccelY,AllbsAccelZ);

%% Volley Forehand (57 shots)
Filename1='00858_CalInertialAndMag.csv';% Disha
Filename2='00860_CalInertialAndMag.csv';% Belen
[AllvfGyroX,AllvfGyroY,AllvfGyroZ,AllvfAccelX,AllvfAccelY,AllvfAccelZ] = Compile_Volley(Filename1,Filename2);
[vfaMax,vfaMin,vfaMean,vfaStd,vfaArea,vfgMax,vfgMin,vfgMean,vfgStd,vfgArea]= MaxMin(AllvfGyroX,AllvfGyroY,AllvfGyroZ,AllvfAccelX,AllvfAccelY,AllvfAccelZ);
[AllvfGyro_av, AllvfAccel_av, LinSpeedvf,thetah_vf,thetal_vf,magAlow_vf,magAhigh_vf] = template(AllvfGyroX,AllvfGyroY,AllvfGyroZ,AllvfAccelX,AllvfAccelY,AllvfAccelZ);

%% Volley Backhand (58 shots)
Filename1='00859_CalInertialAndMag.csv';% Disha
Filename2='00862_CalInertialAndMag.csv';% Belen
[AllvbGyroX,AllvbGyroY,AllvbGyroZ,AllvbAccelX,AllvbAccelY,AllvbAccelZ] = Compile_Volley(Filename1,Filename2);
[vbaMax,vbaMin,vbaMean,vbaStd,vbaArea,vbgMax,vbgMin,vbgMean,vbgStd,vbgArea]= MaxMin(AllvbGyroX,AllvbGyroY,AllvbGyroZ,AllvbAccelX,AllvbAccelY,AllvbAccelZ);
[AllvbGyro_av, AllvbAccel_av, LinSpeedvb,thetah_vb,thetal_vb,magAlow_vb,magAhigh_vb] = template(AllvbGyroX,AllvbGyroY,AllvbGyroZ,AllvbAccelX,AllvbAccelY,AllvbAccelZ);

%% Serve All (66 shots)
Filename1='00057_CalInertialAndMag.csv';% Disha
Filename2='00057_CalInertialAndMag.csv';% Disha
Filename3='00067_CalInertialAndMag.csv';% Katarina and Hannah
Filename4='00070_CalInertialAndMag.csv';% Thomas
[AllsGyroX,AllsGyroY,AllsGyroZ,AllsAccelX,AllsAccelY,AllsAccelZ]=Compile(Filename1,Filename2,Filename3,Filename4);
[saMax,saMin,saMean,saStd,saArea,sgMax,sgMin,sgMean,sgStd,sgArea]= MaxMin(AllsGyroX,AllsGyroY,AllsGyroZ,AllsAccelX,AllsAccelY,AllsAccelZ);
[AllsGyro_av, AllsAccel_av, LinSpeeds,thetah_s,thetal_s,magAlow_s,magAhigh_s] = template(AllsGyroX,AllsGyroY,AllsGyroZ,AllsAccelX,AllsAccelY,AllsAccelZ);

%% Vertical Catonation
aMaxAll=vertcat(faMax(2:101,:),baMax(2:101,:),fsaMax(2:151,:),bsaMax(2:101,:),vfaMax(2:51,:),vbaMax(2:51,:),saMax(2:61,:));
aMinAll=vertcat(faMin(2:101,:),baMin(2:101,:),fsaMin(2:151,:),bsaMin(2:101,:),vfaMin(2:51,:),vbaMin(2:51,:),saMin(2:61,:));
aMeanAll=vertcat(faMean(2:101,:),baMean(2:101,:),fsaMean(2:151,:),bsaMean(2:101,:),vfaMean(2:51,:),vbaMean(2:51,:),saMean(2:61,:));
aStdAll=vertcat(faStd(2:101,:),baStd(2:101,:),fsaStd(2:151,:),bsaStd(2:101,:),vfaStd(2:51,:),vbaStd(2:51,:),saStd(2:61,:));
aAreaAll=vertcat(faArea(2:101,:),baArea(2:101,:),fsaArea(2:151,:),bsaArea(2:101,:),vfaArea(2:51,:),vbaArea(2:51,:),saArea(2:61,:));
gMinAll=vertcat(fgMin(2:101,:),bgMin(2:101,:),fsgMin(2:151,:),bsgMin(2:101,:),vfgMin(2:51,:),vbgMin(2:51,:),sgMin(2:61,:));
gMaxAll=vertcat(fgMax(2:101,:),bgMax(2:101,:),fsgMax(2:151,:),bsgMax(2:101,:),vfgMax(2:51,:),vbgMax(2:51,:),sgMax(2:61,:));
gMeanAll=vertcat(fgMean(2:101,:),bgMean(2:101,:),fsgMean(2:151,:),bsgMean(2:101,:),vfgMean(2:51,:),vbgMean(2:51,:),sgMean(2:61,:));
gStdAll=vertcat(fgStd(2:101,:),bgStd(2:101,:),fsgStd(2:151,:),bsgStd(2:101,:),vfgStd(2:51,:),vbgStd(2:51,:),sgStd(2:61,:));
gAreaAll=vertcat(fgArea(2:101,:),bgArea(2:101,:),fsgArea(2:151,:),bsgArea(2:101,:),vfgArea(2:51,:),vbgArea(2:51,:),sgArea(2:61,:));

%% Generate table for training model
%This creates new rows with values corresponding to the stroke category value
Class(1:100,1)=1; %forehand 100
Class(101:200,1)=2; %backhand 100
Class(201:350,1)=3;%forehand slice 150
Class(351:450,1)=4; %backhand slice 100
Class(451:500,1)=5; % forehand volley 50
Class(501:550,1)=6; % backhand volley 50
Class(551:610,1)=7; %serve

fullArray=horzcat(aMaxAll,aMinAll,aMeanAll,aStdAll,aAreaAll,gMinAll,gMaxAll,gMeanAll,gStdAll,gAreaAll,Class);
means=mean(fullArray);
stds=std(fullArray);
for i=1:size(fullArray,2)-1
normfullArray(:,i)=(fullArray(:,i)-means(1,i))/stds(1,i);
end
normfullArray2=horzcat(normfullArray,Class);
colNames={'aXmax','aYmax','aZmax','aXmin','aYmin','aZmin','aXmean','aYmean','aZmean','aXstd','aYstd','aZstd','aXArea','aYArea','aZArea','gXmax','gYmax','gZmax','gXmin','gYmin','gZmin','gXmean','gYmean','gZmean','gXstd','gYstd','gZstd','gXArea','gYArea','gZArea','Class'};
completeTable=array2table(normfullArray2,'VariableNames',colNames);
%% Generate table for testing trained model
%And also add a coloumn to show which class/type of stroke it is
t_1=zeros(842,1);
t_1(1:126,1)=1; %forehand 126
t_1(127:265,1)=2; %backhand 139
t_1(266:539,1)=3; %forehand slice 274
t_1(540:661,1)=4;%backhand slice 122
t_1(662:718,1)=5; %volleyforehand 57
t_1(719:776,1)=6; % volley backhand 58
t_1(777:842,1)=7; % serve 66

aMaxAll=vertcat(faMax,baMax,fsaMax,bsaMax,vfaMax,vbaMax,saMax);
aMinAll=vertcat(faMin,baMin,fsaMin,bsaMin,vfaMin,vbaMin,saMin);
aMeanAll=vertcat(faMean,baMean,fsaMean,bsaMean,vfaMean,vbaMean,saMean);
aStdAll=vertcat(faStd,baStd,fsaStd,bsaStd,vfaStd,vbaStd,saStd);
aAreaAll=vertcat(faArea,baArea,fsaArea,bsaArea,vfaArea,vbaArea,saArea);
gMinAll=vertcat(fgMin,bgMin,fsgMin,bsgMin,vfgMin,vbgMin,sgMin);
gMaxAll=vertcat(fgMax,bgMax,fsgMax,bsgMax,vfgMax,vbgMax,sgMax);
gMeanAll=vertcat(fgMean,bgMean,fsgMean,bsgMean,vfgMean,vbgMean,sgMean);
gStdAll=vertcat(fgStd,bgStd,fsgStd,bsgStd,vfgStd,vbgStd,sgStd);
gAreaAll=vertcat(fgArea,bgArea,fsgArea,bsgArea,vfgArea,vbgArea,sgArea);
fA=horzcat(aMaxAll,aMinAll,aMeanAll,aStdAll,aAreaAll,gMinAll,gMaxAll,gMeanAll,gStdAll,aAreaAll,t_1);
%Normalise features
mns=mean(fA);
stds=std(fA);
for i=1:size(fA,2)-1
nfA(:,i)=(fA(:,i)-mns(1,i))/stds(1,i);
end
nfA2=horzcat(nfA,t_1);
colNames={'aXmax','aYmax','aZmax','aXmin','aYmin','aZmin','aXmean','aYmean','aZmean','aXstd','aYstd','aZstd','aXArea','aYArea','aZArea','gXmax','gYmax','gZmax','gXmin','gYmin','gZmin','gXmean','gYmean','gZmean','gXstd','gYstd','gZstd','gXArea','gYArea','gZArea','Class'};
checkTable=array2table(nfA2,'VariableNames',colNames);
checkTable2=checkTable(:,1:30);
%%
load mediumSVM_largeSet.mat
yfit = mediumSVM_largeSet.predictFcn(checkTable2)
diff=t_1-yfit;
count=nnz(diff);
Accu=1-(count/length(t_1));





function [SignalX,SignalY,SignalZ,SignalTime] = segmentVolley(Filename)
%Backhand data set
bData=dlmread(Filename,',',1,0);%import the csv file, shifting the column down by one to avoid reading titles as numeric values,defining the separator of a csv file by using ',' 
bPacketNumber=bData(:,1);
bTimedomain=bPacketNumber./128; % because the frequency used is 128Hz
bGyroX=bData(:,2);
bGyroY=bData(:,3);
bGyroZ=bData(:,4);

%plot(bTimedomain, bGyroX,'r',bTimedomain, bGyroY,'g',bTimedomain, bGyroZ, 'b');

%% Absolute magnitude of gyro data and curve smoothing
bGyroMean=sqrt((bGyroX.^2)+(bGyroY.^2)+(bGyroZ.^2)); % absolute magnitude backhand
windowSize=40;
bGyroMeanMovav = tsmovavg(bGyroMean,'s',windowSize,1); % moving average backhand
bGyroMeanSmooth=smooth(bGyroMean); % cure smoothing backhand
[bpks,blocs] = findpeaks(bGyroMeanMovav,'MinPeakProminence',200,'MinPeakDistance',252,'MinPeakHeight',300); % peak distance of 2s and min peak height of 300
%
% figure
% plot(bTimedomain, bGyroMeanMovav,bTimedomain(blocs),bpks,'or');
%xlim([180 300]);

%% Saving each shot into separate column of one big array
% shot length is assumed to be 5s in length

SignalTime=zeros(433,length(bpks));
SignalX=zeros(433,length(bpks)); % array to store each shot in one column, so 33 columns for 33 shots and 1081 rows for 1081 data points which represent 5s = 1 shot
SignalY=zeros(433,length(bpks));
SignalZ=zeros(433,length(bpks));

for j=1:length(bpks)
     timeIndex=blocs(j); % select first time value of peak
     startSignal=timeIndex-216; % subtract 2.3s worth od data points from peak to obtian time when shot begins
     endSignal=timeIndex+216; % add 2.5s worth of data points from peak to obtain end of signal
     SignalTime(:,j) = bTimedomain(startSignal:endSignal); % 1 shot in time index to be saved in Signal matrix
     SignalX(:,j) = bGyroX(startSignal:endSignal);
     SignalY(:,j) = bGyroY(startSignal:endSignal);
     SignalZ(:,j) = bGyroZ(startSignal:endSignal);
end
% figure
% hold on
% for plotIdx = 1:size(SignalX,2)
%     plot(SignalX(:,plotIdx),'r') % overlay all forehand shots onto 1 curve
%     plot(SignalY(:,plotIdx),'g') % overlay all forehand shots onto 1 curve
%     plot(SignalZ(:,plotIdx),'b') % overlay all forehand shots onto 1 curve    
% end
% xlabel('Time (s)'); %x-axis label 
% set(gca,'XTickLabel',{'1','2','3','4',},'XTick',[126 252 378 504],'Fontsize',14);
% ylabel('Gyroscope (°/s)'); %y-asix label
% legend('\omega_x','\omega_y','\omega_z')
% legend boxoff
end

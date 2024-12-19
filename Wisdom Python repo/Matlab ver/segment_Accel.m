function [SignalX,SignalY,SignalZ,SignalTime] = segment_Accel(Filename)

%Backhand data set
bData=dlmread(Filename,',',1,0);%import the csv file, shifting the column down by one to avoid reading titles as numeric values,defining the separator of a csv file by using ',' 
bPacketNumber=bData(:,1);
bTimedomain=bPacketNumber./128; % because the frequency used is 128Hz
bGyroX=bData(:,2);
bGyroY=bData(:,3);
bGyroZ=bData(:,4);
bAccelerationX=bData(:,5);
bAccelerationY=bData(:,6);
bAccelerationZ=bData(:,7);

%plot(bTimedomain, bGyroX,'r',bTimedomain, bGyroY,'g',bTimedomain, bGyroZ, 'b');

%% Absolute magnitude of gyro data and curve smoothing
bGyroMean=sqrt((bGyroX.^2)+(bGyroY.^2)+(bGyroZ.^2)); % absolute magnitude backhand
windowSize=40;
bGyroMeanMovav = tsmovavg(bGyroMean,'s',windowSize,1); % moving average backhand
[bpks,blocs] = findpeaks(bGyroMeanMovav,'MinPeakProminence',200,'MinPeakDistance',252,'MinPeakHeight',300); % peak distance of 2s and min peak height of 300
%
%figure
%plot(bTimedomain, bGyroMeanMovav,bTimedomain(blocs),bpks,'or');
%xlim([180 300]);

%% Saving each shot into separate column of one big array
% shot length is assumed to be 5s in length

SignalTime=zeros(505,length(bpks));
SignalX=zeros(505,length(bpks)); % array to store each shot in one column, so 33 columns for 33 shots and 1081 rows for 1081 data points which represent 5s = 1 shot
SignalY=zeros(505,length(bpks));
SignalZ=zeros(505,length(bpks));

for j=1:length(bpks)
     timeIndex=blocs(j); % select first time value of peak
     startSignal=timeIndex-252; % subtract 2s worth od data points from peak to obtian time when shot begins
     endSignal=timeIndex+252 ;% add 2s worth of data points from peak to obtain end of signal
               if j==1
         startSignal=1;
         endSignal=505;
        else if j==length(bpks)
          startSignal=length(bTimedomain)-504;
          endSignal=length(bTimedomain);
         end
     end
     SignalTime(:,j) = bTimedomain(startSignal:endSignal); % 1 shot in time index to be saved in Signal matrix
     SignalX(:,j) = bAccelerationX(startSignal:endSignal);
     SignalY(:,j) = bAccelerationY(startSignal:endSignal);
     SignalZ(:,j) = bAccelerationZ(startSignal:endSignal);
end
% figure
% hold on
% for plotIdx = 1:size(SignalX,2)
%     plot(SignalX(:,plotIdx),'r'); % overlay all forehand shots onto 1 curve
%     plot(SignalY(:,plotIdx),'g'); % overlay all forehand shots onto 1 curve
%     plot(SignalZ(:,plotIdx),'b'); % overlay all forehand shots onto 1 curve
%     legend('a_x','a_y','a_z')
% end
% xlabel('Time (s)'); %x-axis label 
% set(gca,'XTickLabel',{'1','2','3','4',},'XTick',[126 252 378 504],'Fontsize',18);
% ylabel('Acceleration (g)'); %y-asix label
% legend boxoff

end

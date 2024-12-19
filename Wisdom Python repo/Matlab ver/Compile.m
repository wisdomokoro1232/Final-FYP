function [AllfGyroX,AllfGyroY,AllfGyroZ,AllfAccelX,AllfAccelY,AllfAccelZ] = Compile(Filename1,Filename2,Filename3,Filename4)
%To run this function you will want to type in Compile(Filename1,Filename2,Filename3,Filename4)
%After declaring the filenames
% Compile forehands
[DfGyroX,DfGyroY,DfGyroZ,DfGyroTime]= segment_Gyro(Filename1);
[DfAccelX,DfAccelY,DfAccelZ,DfAccelTime]= segment_Accel(Filename1);

[HfGyroX,HfGyroY,HfGyroZ,HfGyroTime]= segment_Gyro(Filename2);
[HfAccelX,HfAccelY,HfAccelZ,HfAccelTime]= segment_Accel(Filename2);

[KfGyroX,KfGyroY,KfGyroZ,KfGyroTime]= segment_Gyro(Filename3);
[KfAccelX,KfAccelY,KfAccelZ,KfAccelTime]= segment_Accel(Filename3);

[TfGyroX,TfGyroY,TfGyroZ,TfGyroTime]= segment_Gyro(Filename4);
[TfAccelX,TfAccelY,TfAccelZ,TfAccelTime]= segment_Accel(Filename4);

%%
AllfGyroX=horzcat(DfGyroX,HfGyroX,KfGyroX,TfGyroX);
AllfGyroY=horzcat(DfGyroY,HfGyroY,KfGyroY,TfGyroY);
AllfGyroZ=horzcat(DfGyroZ,HfGyroZ,KfGyroZ,TfGyroZ);
AllfAccelX=horzcat(DfAccelX,HfAccelX,KfAccelX,TfAccelX);
AllfAccelY=horzcat(DfAccelY,HfAccelY,KfAccelY,TfAccelY);
AllfAccelZ=horzcat(DfAccelZ,HfAccelZ,KfAccelZ,TfAccelZ);
% figure
% hold on
% for plotIdx = 1:size(AllfGyroX,2)
%     plot(AllfGyroX(:,plotIdx),'r'); % overlay all forehand shots onto 1 curve
%     plot(AllfGyroY(:,plotIdx),'g'); % overlay all forehand shots onto 1 curve
%     plot(AllfGyroZ(:,plotIdx),'b'); % overlay all forehand shots onto 1 curve    
% end
% xlabel('Time (s)'); %x-axis label 
% set(gca,'XTickLabel',{'1','2','3','4',},'XTick',[126 252 378 504]);
% ylabel('Gyroscope (°/s)'); %y-asix label
% 
% figure
% hold on
% for plotIdx = 1:size(AllfAccelX,2)
%     plot(AllfAccelX(:,plotIdx),'r'); % overlay all forehand shots onto 1 curve
%     plot(AllfAccelY(:,plotIdx),'g'); % overlay all forehand shots onto 1 curve
%     plot(AllfAccelZ(:,plotIdx),'b'); % overlay all forehand shots onto 1 curve    
% end
% xlabel('Time (s)'); %x-axis label 
% set(gca,'XTickLabel',{'1','2','3','4',},'XTick',[126 252 378 504]);
% ylabel('Acceleration (g)'); %y-asix label
end

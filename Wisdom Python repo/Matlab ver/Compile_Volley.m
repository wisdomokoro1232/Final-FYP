function [AllfGyroX,AllfGyroY,AllfGyroZ,AllfAccelX,AllfAccelY,AllfAccelZ] = Compile(Filename1,Filename2)
% Compile forehands
[DfGyroX,DfGyroY,DfGyroZ,DfGyroTime]= segment_Gyro(Filename1);
[DfAccelX,DfAccelY,DfAccelZ,DfAccelTime]= segment_Accel(Filename1);

[HfGyroX,HfGyroY,HfGyroZ,HfGyroTime]= segment_Gyro(Filename2);
[HfAccelX,HfAccelY,HfAccelZ,HfAccelTime]= segment_Accel(Filename2);

%%
AllfGyroX=horzcat(DfGyroX,HfGyroX);
AllfGyroY=horzcat(DfGyroY,HfGyroY);
AllfGyroZ=horzcat(DfGyroZ,HfGyroZ);
AllfAccelX=horzcat(DfAccelX,HfAccelX);
AllfAccelY=horzcat(DfAccelY,HfAccelY);
AllfAccelZ=horzcat(DfAccelZ,HfAccelZ);
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

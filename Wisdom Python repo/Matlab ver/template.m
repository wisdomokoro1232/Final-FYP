function [AllfGyro_av, AllfAccel_av, LinSpeed, theta_high, theta_low,magA_low,magA_high] = template(AllfGyroX,AllfGyroY,AllfGyroZ,AllfAccelX,AllfAccelY,AllfAccelZ)
% Angular Velocities

AllfGyro_av(:,1) = mean(AllfGyroX,2);
AllfGyro_av(:,2) = mean(AllfGyroY,2);
AllfGyro_av(:,3) = mean(AllfGyroZ,2);
%Racket linear speed
R = 0.7445; %radius from shoulder to point of impact of ball
Maxes = max(abs(AllfGyro_av));
Peaky= Maxes(1,2);
Peakz = Maxes(1,3);
omega=sqrt((Peaky*0.0174533)^2 + (Peakz*0.0174533)^2);
LinSpeed = omega * R;
%Spin Rating
maxiY=max(abs(AllfGyroY));
maxY = max(maxiY);
minY = min(maxiY);
maxiZ=max(abs(AllfGyroZ));
maxZ = max(maxiZ);
minZ = min(maxiZ);
omega_high = sqrt(maxY^2 + maxZ^2);
omega_low = sqrt(minY^2 + minZ^2);
theta_high = omega_high*0.12;
theta_low = omega_low*0.12;

figure
plot(AllfGyro_av(:,1),'r','LineWidth',1.5)
hold on
plot(AllfGyro_av(:,2),'g','LineWidth',1.5)
plot(AllfGyro_av(:,3),'b','LineWidth',1.5)
legend('\omega_x','\omega_y','\omega_z')
legend boxoff
xlabel('Time (s)','Fontsize',14); %x-axis label 
set(gca,'XTickLabel',{'1','2','3','4',},'XTick',[126 252 378 504],'Fontsize',17);
ylabel('Gyroscope (°/s)','Fontsize',17); %y-asix label



%Acceleration mag for Power Rating
AllfAccel_av(:,1) = mean(AllfAccelX,2);
AllfAccel_av(:,2) = mean(AllfAccelY,2);
AllfAccel_av(:,3) = mean(AllfAccelZ,2);
MagAccel = sqrt(AllfAccelZ.^2); % magnitude of acceleration for all shots + AllfAccelY.^2 + AllfAccelX.^2
MagAccelPeaks = MagAccel(229:237,:);
MagAccelmeans = mean(MagAccelPeaks);
magA_low = min(MagAccelmeans(2:end-2));
magA_high = max(MagAccelmeans(2:end-2));




% figure
% plot(AllfAccel_av(:,1),'r','LineWidth',1.5)
% hold on
% plot(AllfAccel_av(:,2),'g','LineWidth',1.5)
% plot(AllfAccel_av(:,3),'b','LineWidth',1.5)
% legend('a_x','a_y','a_z')
% xlabel('Time (s)','Fontsize',14); %x-axis label 
% set(gca,'XTickLabel',{'1','2','3','4',},'XTick',[126 252 378 504],'Fontsize',13);
% ylabel('Acceleration (g)','Fontsize',14); %y-asix label

end


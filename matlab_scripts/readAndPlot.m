function [t, data] = readAndPlot(varargin)

if length(varargin)> 3
    error('Only three input args allowed')
end

optargs = {'./TestResults6/','timedata.txt','RPS_TimeResponse1.txt'};
optargs(1:length(varargin)) = varargin;
[directory, tfilename, filename] = optargs{:};
disp(directory);
disp(filename);
disp(tfilename);

fileID = fopen([directory tfilename],'r');



formatSpec = '%f';

t = fscanf(fileID,formatSpec);
fclose(fileID);

count = 1;
data = zeros(length(t),4);

while (count <5)
    filename(end - length('.txt')) = num2str(count);
    fileID = fopen([directory filename],'r');
    data(:,count) = fscanf(fileID,formatSpec);
    fclose(fileID);
    figure(2)
    subplot(2,2,count);
    plot(t,data(:,count));
    title(['Motor ' num2str(count)])
    ylabel('Speed (Rotations Per Second)')
    xlabel('Time (s)')
    count = count + 1;
    
end

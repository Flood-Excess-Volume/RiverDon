%%% Script carries out the following:
%
% > loads and extracts relevant flow-data for Sheffield Hadfields
% > calculates rating curve from empirical formula
% > computes FEV and duration etc.
% > plots data using subroutines:
% <plot3panel.m>
% <plotFEVhT.m>
% <plot_h_year.m>
% <plot_ratingcurve.m>

% TK, August 2018 - adapted from OB's <flowdatafloodsshef.m>

clear;

%% DATA: load + extract

% Sheffield Hadfields Flow 15 min Jan 07 to Dec 07.csv
%
%
% Flood data analysis:
%
% Sheffiel Don River excel files: 22 to 35061
%
armleyexc = [22, 35061]; % rows in .csv file where data lies
nlenarmleyfi = armleyexc(2)-armleyexc(1)+1;
armleymeimaartdayspmo = [31,28,31,30,31,30,31,31,30,31,30,31]; % 2007
day15min = 24*4;
daysfromjan = 31+28+31+30+31-1.0; %daysfromjan = 0.0;
no15minarmley = (sum(armleymeimaartdayspmo))*day15min;
fprintf('number 15min intervals Jan 2007 to Dec 2007 Sheff Hadfields flood gauge: %g %g\n',no15minarmley,nlenarmleyfi);
ndecarmley(1:2) = [(sum(armleymeimaartdayspmo(1:5))+24), (sum(armleymeimaartdayspmo(1:6))-2)]*day15min;
%

%%

fid = fopen('Sheffield Hadfields Flow 15 min Jan 07 to Dec 07.csv');
dataflow = textscan(fid, '%s %f %s %s %s %s %s %s %s %s', 'Delimiter', ',', 'HeaderLines', 21);
fclose(fid);

fid2 = fopen('Sheffield Hadfields Stage 15 min Jan 07 to Dec 07.csv');
datastage = textscan(fid2, '%s %f %s %f %f %s %f %s %s %s %s %s %s %s', 'Delimiter', ',', 'HeaderLines', 21);
fclose(fid2);

% extract Q data
timestampQ = datetime(dataflow{1},'InputFormat','dd/MM/yyyy HH:mm:SS');
nq = length(dataflow{2});
timeQ = zeros(1,nq);
dischargeQ = zeros(1,nq);
for ii = 1:nq
    timeQ(ii) = 0.25*ii/24; % Times 0.25 gives hours, 1/24 gives day
    dischargeQ(ii) = dataflow{2}(ii);
end

% extract h data
timestamph = datetime(datastage{1},'InputFormat','dd/MM/yyyy HH:mm:SS');
nh = length(datastage{2});
timeh = zeros(1,nh);
stage = zeros(1,nh);
for ii = 1:nh
    timeh(ii) = 0.25*ii/24;
    stage(ii) = datastage{2}(ii);
end

%% Rating curve
arml = [0, 0.52, 0.931, 1.436]; % lower stage limit
armu = [0.52,0.931,1.436,3.58]; % upper stage limit
se = [0.197, 0.197, 0.0801, 0.0801]; % SE

%rc coeffs
Crc = [78.4407,77.2829,79.5956,41.3367];
brc = [1.7742,1.3803,1.2967,1.1066];
arc = [0.223,0.3077,0.34,-0.5767];

Ns = 10000;
[armlevc,ic] = max(stage);
rcstage = arml(1):(armlevc-arml(1))/Ns:armlevc;
[armlevc,ic] = max(rcstage);

rcdischarge = rcstage; % Q for rating curve
rcdischargeL = rcstage;
rcdischargeU = rcstage;

discharge = stage;
dischargeL = stage;
dischargeU = stage;

%%
% % Q = Q(h)
for ii = 1:Ns+1
    
    if (rcstage(ii) <= armu(1)) && (rcstage(ii) >= arml(1))
        
        rcdischarge(ii) = real(Crc(1)*(rcstage(ii)-arc(1))^brc(1));
        rcdischargeL(ii) = (1.0-se(1))*rcdischarge(ii); % -SE
        rcdischargeU(ii) = (1.0+se(1))*rcdischarge(ii); % +SE
        
    elseif (rcstage(ii) <= armu(2)) && (rcstage(ii) > arml(2))
        
        rcdischarge(ii) = Crc(2)*(rcstage(ii)-arc(2))^brc(2);
        rcdischargeL(ii) = (1.0-se(2))*rcdischarge(ii); % -SE
        rcdischargeU(ii) = (1.0+se(2))*rcdischarge(ii); % +SE
        
    elseif (rcstage(ii) <= armu(3)) && (rcstage(ii) > arml(3))
        
        rcdischarge(ii) = Crc(3)*(rcstage(ii)-arc(3))^brc(3);
        rcdischargeL(ii) = (1.0-se(3))*rcdischarge(ii); % -SE
        rcdischargeU(ii) = (1.0+se(3))*rcdischarge(ii); % +SE

    elseif (rcstage(ii) > armu(3))
        
        rcdischarge(ii) = Crc(4)*(rcstage(ii)-arc(4))^brc(4);
        rcdischargeL(ii) = (1.0-se(4))*rcdischarge(ii); % -SE
        rcdischargeU(ii) = (1.0+se(4))*rcdischarge(ii); % +SE
        
    end
    
end

% Q = Q(h(t)) = Q(t)
for ii = 1:nh
    
    if (stage(ii) <= armu(1)) && (stage(ii) >= arml(1))
        
        discharge(ii) = Crc(1)*(stage(ii)-arc(1))^brc(1);
        dischargeL(ii) = (1.0-se(1))*discharge(ii); % -SE
        dischargeU(ii) = (1.0+se(1))*discharge(ii); % +SE
        
    elseif (stage(ii) <= armu(2)) && (stage(ii) > arml(2))
        
        discharge(ii) = Crc(2)*(stage(ii)-arc(2))^brc(2);
        dischargeL(ii) = (1.0-se(2))*discharge(ii); % -SE
        dischargeU(ii) = (1.0+se(2))*discharge(ii); % +SE
        
    elseif (stage(ii) <= armu(3)) && (stage(ii) > arml(3))
        
        discharge(ii) = Crc(3)*(stage(ii)-arc(3))^brc(3);
        dischargeL(ii) = (1.0-se(3))*discharge(ii); % -SE
        dischargeU(ii) = (1.0+se(3))*discharge(ii); % +SE
        
    elseif (stage(ii) > armu(3))
        
        discharge(ii) = Crc(4)*(stage(ii)-arc(4))^brc(4);
        dischargeL(ii) = (1.0-se(4))*discharge(ii); % -SE
        dischargeU(ii) = (1.0+se(4))*discharge(ii); % +SE
        
    end
    
end

%% Calculate FEV etc
% Sheffield gauge flow and levels
%
armin = 2.0;
armax = 4.6750; % 4.75;
Na = 20;
da = 0.1; % (armax-armin)/Na;
armstep = armin:da:armax;
Na = size(armstep,2);
nle = size(stage(ndecarmley(1):ndecarmley(2)),2);
arnle = zeros(1,nle);
for nna = 1:Na
    armcrit = armstep(nna); % m
    [harmax,iarmax] = max(stage(ndecarmley(1):ndecarmley(2)));
    [harmup,iarmup] = min(abs(stage(ndecarmley(1):ndecarmley(1)+iarmax)-armcrit));
    [harmdo,iarmdo] = min(abs(stage(ndecarmley(1)+iarmax:ndecarmley(2))-armcrit));
    iarmdo = iarmax+iarmdo;
    %
    %
    flowarmcrit = discharge(ndecarmley(1)+iarmup-1);
    armexcessvol = 15*60*sum( discharge(ndecarmley(1)+iarmup-1:ndecarmley(1)+iarmdo-1)-flowarmcrit ); % 15min
    armexcvol(nna) = armexcessvol;
    flowarmcrit = Crc(4)*(armcrit-arc(4))^brc(4);
    posarm = max(discharge(ndecarmley(1):ndecarmley(2))-flowarmcrit,arnle);
    armexcessvol = 15*60*sum(posarm);
    flowarmcritvec(nna) = Crc(4)*(armcrit-arc(4))^brc(4);
    Tfvec(nna) = 15*60*nnz(posarm);
    armexcvol(nna) = armexcessvol;
end

%%
armcrit = 2.9; % hT = 2.9; % 4.3337; % 2.9; % m 2.92m at Ladys Bridge Sheffield

QT = Crc(4)*(armcrit-arc(4))^brc(4);
QTminus = QT*(1-se(4));
QTplus = QT*(1+se(4));

flowarmcrit = Crc(4)*(armcrit-arc(4))^brc(4);
posarm = max(discharge(ndecarmley(1):ndecarmley(2))-flowarmcrit,arnle);

posarm = max(discharge(ndecarmley(1):ndecarmley(2))-QT,arnle);
posarmL = max(dischargeL(ndecarmley(1):ndecarmley(2))-QTplus,arnle);
posarmU = max(dischargeU(ndecarmley(1):ndecarmley(2))-QTminus,arnle);

% FEVs
armexcessvol = 15*60*sum(posarm);
armexcessvolL = 15*60*sum(posarmL); 
armexcessvolU = 15*60*sum(posarmU);

% flood durations
Tf = 15*60*nnz(posarm);
TfL = 15*60*nnz(posarmL);
TfU = 15*60*nnz(posarmU);

% mean Q and h
Qm = QT+armexcessvol/Tf; 
hm = (Qm/Crc(4))^(1/brc(4))+arc(4);
%

[harmax,iarmax] = max(stage(ndecarmley(1):ndecarmley(2)));
[harmup,iarmup] = min(abs(stage(ndecarmley(1):ndecarmley(1)+iarmax)-armcrit));
[harmdo,iarmdo] = min(abs(stage(ndecarmley(1)+iarmax:ndecarmley(2))-armcrit));
iarmdo = iarmax+iarmdo;

armeymean = 0.5*(max(stage)+armcrit);
armexcessvolest = max(discharge)*(armeymean/max(stage))*(max(stage)-armcrit)/max(stage)*(iarmdo-iarmup)*0.25*3600;
armexcessvolest2 = max(discharge)*(armeymean/max(stage))*(max(stage)-armeymean)/max(stage)*(iarmdo-iarmup)*0.25*3600;



%% data for plotting panel plot

t = timeh(ndecarmley(1):ndecarmley(2))-daysfromjan; % time
h = stage(ndecarmley(1):ndecarmley(2)); % h data
q = dischargeQ(ndecarmley(1):ndecarmley(2)); % q data

q2 = discharge(ndecarmley(1):ndecarmley(2));
q2L = dischargeL(ndecarmley(1):ndecarmley(2));
q2U = dischargeU(ndecarmley(1):ndecarmley(2));

hrc = rcstage; % h rating curve
qrc = rcdischarge; % q rating curve

%% Tf as a function of QT
here = find(Tfvec == Tf);
dTfdQT = (Tfvec(here+1) - Tfvec(here-1))/(flowarmcritvec(here+1) - flowarmcritvec(here-1));
x = linspace(flowarmcritvec(here-5),flowarmcritvec(here+5),11);
y = dTfdQT*(x - QT) + Tf;
plot(flowarmcritvec, Tfvec,'k'); hold on;
% plot([QT, QT],[Tf,Tfvec(end)],'k:');
% plot([flowarmcritvec(1),QT],[Tf, Tf],'k:');
plot(x,y,'r','linewidth',2);
plot(QT,Tf,'or','linewidth',2);
text(1.01*QT,1.01*Tf,'$(Q_T, T_f)$','fontsize',16, 'HorizontalAlignment', 'left','Interpreter','latex');
% text(0.9*QT,0.9*Tf,'$$\frac{\partial Q_T}{\partial T_f)$$','fontsize',16, 'HorizontalAlignment', 'left','Interpreter','latex');
xlabel('$Q_T$ [m$^3$/s]','fontsize',16,'Interpreter','latex');
ylabel('$T_f$ [s]','fontsize',16,'Interpreter','latex');

%% error tests
sd = max(se);
sd = 0.080;
dt = 15*60;
qk = q(q>QT);
q2k = q2(q2>QT);

Ve = armexcessvol;
dVedTf = Ve/Tf;

% both ignoring Tf contributions
errVe2 = dt^2*sd^2*sum(qk.^2) + Tf^2*sd^2*QT^2; %applying rc N+1 times (Qk for k=1,...,N and QT)
errVm2 = Tf^2*sd^2*Qm^2 + Tf^2*sd^2*QT^2; % applying rc 1+1 times (Qm and QT)

% both including Tf contributions
errVe2 = dt^2*sd^2*sum(qk.^2) + (Tf^2 + dVedTf^2*dTfdQT^2)*sd^2*QT^2; %applying rc N+1 times (Qk for k=1,...,N and QT)
errVm2 = Tf^2*sd^2*Qm^2 + (Tf^2 + dVedTf^2*dTfdQT^2)*sd^2*QT^2; % applying rc 1+1 times (Qm and QT)

errVe = sqrt(errVe2);
errVm = sqrt(errVm2);

errVefrac = errVe/Ve
errVmfrac = errVm/Ve

%% plotting routines

% 3 panel with h(t), Q(h), Q(t)
plot3panel;
plot3panelerr;

% FEV and sidelength as a function of threshold
plotFEVhT;

% h(t) for whole year
plot_h_year;

% rating curve and discharge with errors
plot_ratingcurve;
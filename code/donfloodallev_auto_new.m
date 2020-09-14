%%%%
% Generate winter/summer flood ecxcess lake figures for given scenarios etc.
% (suceeds <donalllev_auto.m>)
%%%%

% Used to generate fig. 9 in Bokhove, Kelmanson, & Kent (2018).
% On using flood-excess volume to assess natural flood management,
% exemplified for extreme 2007 and 2015 floods in Yorkshire.
% https://doi.org/10.31223/osf.io/87z6w

%%% To use as it is:
% - choose season nws below and run as normal

%%% To edit for different FEVs scenarios, etc.:
% - change inputs in the next section

%%% To change plotting attributes, e.g., location of text/arrows, shading
% - top of PLOTTING section below


clear; clf;

nws = 1; % summer
% nws = 0; % winter

%% SCENARIOS AND STORAGE
scens = {'S1', 'S2a', 'S2b', 'S2c', 'S3a', 'S3b', 'S3c'}; % scenario names
nopto = length(scens); % # of scenarios
narea = 3; % # of areas
FEV = 3.000; % M cubic metres

depth = 2; % m
Lside = sqrt(FEV*10^6/depth);
xmax = Lside;
Vr = 2.8;     % M cubic metres (res stroage)
Vnfm = 0.567; % M cubic metres (nfm storage)
V3 = [2.8 0 0.567];

vectopto = 1.0*ones(1,nopto);
vectFEV = FEV*ones(1,narea);
Ama = zeros(nopto,narea);

Astore = Ama;
Ama(1,1:3) = [1/3 1/3 1/3]; % S1
Ama(2,1:3) = [1/2 1/2 0];% S2a
Ama(3,1:3) = [0 1/2 1/2];% S2b
Ama(4,1:3) = [1/2 0 1/2];% S2c
Ama(5,1:3) = [1 0 0];% S3a
Ama(6,1:3) = [0 1 0];% S3b
Ama(7,1:3) = [0 0 1];% S3c

Arain = Ama*FEV;
Astore(:,1) = Vr;
Astore(:,2) = 0.0;
Astore(:,3) = Vnfm;
Astore;

Aactstore = min(Astore,Arain)
Vsum = Aactstore*ones(narea,1)
VsF = Vsum/FEV 
Vfracs = Vsum/FEV; % same as above?

% rainfall probabilities for each scenario
vwinterp = [1/2 1/8 1/8 0 1/12 1/12 1/12]
vsummerp = [1/4 1/12 1/12 1/12 1/6 1/6 1/6]

[nw,dw] = rat(vwinterp); % for plot labelling
[ns,ds] = rat(vsummerp);

Vwp = vwinterp;
Vsp = vsummerp;

for ii = 2:nopto % cumulative probabilities
  Vwp(ii) = Vwp(ii)+Vwp(ii-1);
  Vsp(ii) = Vsp(ii)+Vsp(ii-1);
end

Vwp0 = [0 Vwp];
Vsp0 = [0 Vsp];

%% STATISTICS
% Average
vwintav = Vfracs'*transpose(vwinterp) % rain scenarios with weights
vsummav = Vfracs'*transpose(vsummerp)

rw = vwintav*ones(1,nopto);
rs = vwintav*ones(1,nopto);

% standard deviation
swint = 0.0;
ssumm = 0.0;
for ii=1:nopto
   swint = swint+(Vfracs(ii)*vwinterp(ii)-vwintav)^2;
   ssumm = ssumm+(Vfracs(ii)*vsummerp(ii)-vsummav)^2;
end

devwin = swint/(nopto-1)
devsum = ssumm/(nopto-1)
%
%
% 

%% PLOTTING

fs = 14; % text size
pos = 0.8; % text position in [0,1]
pos_a = 0.95; %arrow position in [0,1]
alph = 0.3; % transparency of shading

figno = 20;

Lx = Lside;
Ly = Lside;
L0 = 0;
x1 = [L0,Lx,Lx,L0,L0,L0,Lx,Lx,L0,L0];
y1 = [0,0,Ly,Ly,0,0,0,Ly,Ly,0];
z1 = [0,0,0,0,0,depth,depth,depth,depth,depth];
x2 = [Lx,Lx]; y2 = [0,0]; z2 = [0,depth];
x3 = [Lx,Lx]; y3 = [Ly,Ly]; z3 = [0,depth];
x4 = [0,0]; y4 = [Ly,Ly]; z4 = [0,depth];


fh3 = figure(figno+nws); clf;

plot(x1,y1,'-k','linewidth',3); hold on;
plot(x2,y2,'-k','linewidth',3); hold on;
plot(x3,y3,'--k','linewidth',3); hold on;
plot(x4,y4,'-k','linewidth',3); hold on;
axis('equal');

if (nws == 0)
    
    x1 = Lx*[ 0 VsF(1) VsF(1) VsF(2) VsF(2) VsF(3) VsF(3) VsF(4) VsF(4) VsF(5) VsF(5) VsF(6) VsF(6) VsF(7) VsF(7) 0];
    y1 = Ly*[ 0 0 Vwp(1) Vwp(1) Vwp(2) Vwp(2) Vwp(3) Vwp(3) Vwp(4) Vwp(4) Vwp(5) Vwp(5) Vwp(6) Vwp(6) Vwp(7) Vwp(7)];
    plot(x1,y1,'-k','linewidth',4); hold on;
    patch(x1,y1,[0 0 0.99]); alpha(alph); hold on;
    
    Lx = vwintav*Lside;
    x1 = [Lx,Lx];
    y1 = [0,Ly];
    plot(x1,y1,'--b','linewidth',2); hold on;
    
    Lx = (vwintav+devwin)*Lside;
    x1 = [Lx,Lx,];
    y1 = [0,Ly];
    
    plot(x1,y1,'-.b','linewidth',1); hold on;
    Lx = (vwintav-devwin)*Lside;
    x1 = [Lx,Lx]; y1 = [0,Ly];
    plot(x1,y1,'-.b','linewidth',1); hold on;
    
    for nn = 1:nopto % annotate arrows for scenario probabilities
        
        an = annotation('doublearrow');
        an.Parent = gca;
        axx = [1 1]*pos_a*Lside;
        axy = [Vwp0(nn) Vwp0(nn+1)]*Lside;
        an.X = axx;
        an.Y = axy;
        an.Color = 'red';
        
        if nw(nn) == 0
%             text(pos*Lside,Lside*(Vwp0(nn)+Vwp0(nn+1))/2, sprintf(' (%s): $$%d$$',scens{nn},nw(nn)),...
%                 'Interpreter','latex','fontsize',fs);
        else
            text(pos*Lside,Lside*(Vwp0(nn)+Vwp0(nn+1))/2, sprintf(' (%s): $$\\frac{%d}{%d}$$',scens{nn}, ...
                nw(nn), dw(nn)),'Interpreter','latex','fontsize',fs);
        end
        
        line([0 Lside],[Lside*Vwp0(nn) Lside*Vwp0(nn)],'Color','r','Linestyle',':');
        
    end
    
    line([0 Lside],[Lside*Vwp0(end) Lside*Vwp0(end)],'Color','r','Linestyle',':');
    
else
    
    x1 = Lx*[ 0 VsF(1) VsF(1) VsF(2) VsF(2) VsF(3) VsF(3) VsF(4) VsF(4) VsF(5) VsF(5) VsF(6) VsF(6) VsF(7) VsF(7) 0];
    y1 = Ly*[ 0 0 Vsp(1) Vsp(1) Vsp(2) Vsp(2) Vsp(3) Vsp(3) Vsp(4) Vsp(4) Vsp(5) Vsp(5) Vsp(6) Vsp(6) Vsp(7) Vsp(7)];
    plot(x1,y1,'-k','linewidth',4); hold on;
    patch(x1,y1,[0 0 0.99]); alpha(alph); hold on;
    
    Lx = vsummav*Lside;
    x1 = [Lx,Lx];
    y1 = [0,Ly];
    plot(x1,y1,'--b','linewidth',2); hold on;
    
    Lx = (vsummav+devsum)*Lside;
    x1 = [Lx,Lx,];
    y1 = [0,Ly];
    plot(x1,y1,'-.b','linewidth',1); hold on;
    
    
    Lx = (vsummav-devsum)*Lside;
    x1 = [Lx,Lx]; y1 = [0,Ly];
    plot(x1,y1,'-.b','linewidth',1); hold on;
    
    
    for nn = 1:nopto
        
        an = annotation('doublearrow');
        an.Parent = gca;
        axx = [1 1]*pos_a*Lside;
        axy = [Vsp0(nn) Vsp0(nn+1)]*Lside;
        an.X = axx;
        an.Y = axy;
        an.Color = 'red';
        
        if ns(nn) == 0
%             text(pos*Lside,Lside*(Vsp0(nn)+Vsp0(nn+1))/2, sprintf(' (%s): $$%d$$',scens{nn},ns(nn)),...
%                 'Interpreter','latex','fontsize',fs);
        else
            text(pos*Lside,Lside*(Vsp0(nn)+Vsp0(nn+1))/2, sprintf(' (%s): $$\\frac{%d}{%d}$$',scens{nn}, ...
                ns(nn), ds(nn)),'Interpreter','latex','fontsize',fs);
        end
        
        line([0 Lside],[Lside*Vsp(nn) Lside*Vsp(nn)],'Color','r','Linestyle',':');
        
    end
    
    line([0 Lside],[Lside*Vsp0(1) Lside*Vsp0(1)],'Color','r','Linestyle',':');
    
end
        
xlabel('Side-length (m)','fontsize',16);
ylabel('Side-length (m)','fontsize',16);
axis([0 xmax 0 xmax 0 depth]);



if (nws==0)
    title(sprintf('Winter flood-excess lake: FEV $$\\approx (%d^2 \\times 2)$$m$$^3 \\approx %.3f$$Mm$$^3$$',...
        round(Lside,0),FEV),'Interpreter','latex','fontsize',20);
    fh3_fname = 'donallev_winter';
else
    title(sprintf('Summer flood-excess lake: FEV $$\\approx (%d^2 \\times 2)$$m$$^3 \\approx  %.3f$$Mm$$^3$$',...
        round(Lside,0),FEV),'Interpreter','latex','fontsize',20);
    fh3_fname = 'donallev_summer';
end

%% SAVE FIGURE
set(fh3, 'PaperUnits', 'centimeters');
x_width = 21;
y_width = 21;
set(fh3, 'PaperPosition', [0 0 x_width y_width]);
saveas(fh3,fullfile(fh3_fname),'jpeg')





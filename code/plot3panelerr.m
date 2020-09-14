%%% Plotting routine: 3-panel flow data h=h(t), Q=Q(h), Q=Q(t)

% NOTE on saving figure from File > Export setup...:
% > Size: width = 25, height = 25, units = centimeters, expand axes to fill
% figure.
% > Rendering: resolution (dpi) = 300

%% scaled data on [0,1]
t_min = floor(min(t));
t_max = ceil(max(t));
dur = t_max - t_min;

h_min = 0;
h_max = ceil(max(h));

q_min = 0;
q_max = 0.5*round(2*max(q)+50, 1, 'significant'); % round up to next multiple of 50


t_scaled = (t - t_min)./(t_max - t_min);

h_scaled = (h - h_min)./(h_max - h_min);
hrc_scaled = (hrc - h_min)./(h_max - h_min);
rcstage_scaled = (rcstage - h_min)./(h_max - h_min);

q_scaled = (q - q_min)./(q_max - q_min);
qrc_scaled = (qrc - q_min)./(q_max - q_min);
rcdischargeL_scaled = (rcdischargeL - q_min)./(q_max - q_min);
rcdischargeU_scaled = (rcdischargeU - q_min)./(q_max - q_min);
q2_scaled = (q - q_min)./(q_max - q_min);
q2L_scaled = (q2L - q_min)./(q_max - q_min);
q2U_scaled = (q2U - q_min)./(q_max - q_min);

hT_sc = (armcrit - h_min)./(h_max - h_min);
hm_sc = (hm - h_min)./(h_max - h_min);
Qm_sc = (Qm - q_min)./(q_max - q_min);
QT_sc = (QT - q_min)./(q_max - q_min);
QTplus_sc = (QTplus - q_min)./(q_max - q_min);
QTminus_sc = (QTminus - q_min)./(q_max - q_min);



ind_m = find(q_scaled - Qm_sc > eps);
ind_m = [ind_m(1)-1 ind_m ind_m(end)+1];
ind_T = find(q_scaled - QT_sc > eps);
ind_T = [ind_T(1)-1 ind_T ind_T(end)+1];
size(ind_T)

%% make plot

fs = 12;
figure(1001);

plot(t_scaled,q2_scaled,'-k','linewidth',1.5); hold on; %Q(t) top right
err2 = fill_between(t_scaled, q2L_scaled, q2U_scaled); hold on;
err2.FaceAlpha = 0.1;
err2.EdgeColor = 'none';
errQT = fill_between(t_scaled(ind_T(1):ind_T(end)), QTminus_sc*ones(size(ind_T)), QTplus_sc*ones(size(ind_T))); hold on;
%     t_scaled>t_scaled(ind_T(1)) & t_scaled<t_scaled(ind_T(end))); hold on;

errQT.FaceAlpha = 0.1;
errQT.EdgeColor = 'none';

plot(-h_scaled, -t_scaled,'-k','linewidth',1.5); hold on; %h(t) bottom left

plot(-hrc_scaled,qrc_scaled,'-k','linewidth',1.5); hold on; % rating curve top left
err = fill_between(-rcstage_scaled, rcdischargeL_scaled, rcdischargeU_scaled); hold on;
err.FaceAlpha = 0.1;
err.EdgeColor = 'none';

plot([0.0,-max(hrc_scaled)],[0.0,max(qrc_scaled)],'--k','linewidth',1);hold on; %linear rating curve

plot([-hT_sc,-hT_sc],[-1,QT_sc],':k','linewidth',1);hold on; % horiz and vert lines for hT, QT, etc ..
plot([-hm_sc,-hm_sc],[-1,Qm_sc],':k','linewidth',1);hold on;
plot([-hT_sc,1],[QT_sc,QT_sc],':k','linewidth',1);hold on;
plot([-hm_sc,1],[Qm_sc,Qm_sc],':k','linewidth',1);hold on;

p = fill_between_rgb(t_scaled,QT_sc*ones(size(t_scaled)),q_scaled,'b');
p.FaceAlpha = 0.1;

plot([t_scaled(ind_T(end)),t_scaled(ind_T(end))],[QT_sc,Qm_sc],'k','linewidth',2);hold on;
plot([t_scaled(ind_T(1)),t_scaled(ind_T(end))],[QT_sc,QT_sc],'k','linewidth',2);hold on;
plot([t_scaled(ind_T(1)),t_scaled(ind_T(1))],[QT_sc,Qm_sc],'k','linewidth',2);hold on;
plot([t_scaled(ind_T(1)),t_scaled(ind_T(end))],[Qm_sc,Qm_sc],'k','linewidth',2);hold on;

plot([t_scaled(ind_T(1)),t_scaled(ind_T(1))],[-0.2,QT_sc],':k','linewidth',1);hold on;
plot([t_scaled(ind_T(end)),t_scaled(ind_T(end))],[-0.2,QT_sc],':k','linewidth',1);hold on;

arr = annotation('doublearrow');
arr.Parent = gca;
arr.X = [t_scaled(ind_T(1)) t_scaled(ind_T(end))];
arr.Y = [-0.15 -0.15];
arr.Color = 'black';
arr.Head1Style = 'vback3';
arr.Head2Style = 'vback3';
arr.Head1Length = 5;
arr.Head2Length = 5;

ax = gca;
ax.XAxisLocation = 'origin';
ax.YAxisLocation = 'origin';
ax.Layer = 'top';
ax.XTick =  [-1:1/h_max:0 1/dur:1/dur:1];
ax.YTick = [-1:1/dur:0 50/q_max:50/q_max:1];
ax.XTickLabel = [h_max:-1:1 t_min:1:t_max];
ax.YTickLabel = [t_max:-1:t_min+1 0:50:q_max];
ax.TickDir ='both';
ax.XLim = [-1.1 1.1];
ax.YLim = [-1.1 1.1];

% 
text(1.05,-0.15,'$t$ [day]','fontsize',fs, 'HorizontalAlignment', 'right','Interpreter','latex');
text(0.05,-1,'$t$ [day]','fontsize',fs, 'HorizontalAlignment', 'left','Interpreter','latex');
text(0.05,1,'$Q$ [m$^3$/s]','fontsize',fs, 'HorizontalAlignment', 'left','Interpreter','latex');
text(-1,0.05,'$\bar{h}$ [m]','fontsize',fs,'HorizontalAlignment', 'center','Interpreter','latex');
text(-hT_sc,-1,'$h_T$','fontsize',fs,'VerticalAlignment', 'top','Interpreter','latex');
text(-hm_sc,-1,'$h_m$','fontsize',fs,'VerticalAlignment', 'top','Interpreter','latex');
text(1,QT_sc,'$Q_T$','fontsize',fs,'VerticalAlignment', 'middle','Interpreter','latex');
text(1,Qm_sc,'$Q_m$','fontsize',fs,'VerticalAlignment', 'middle','Interpreter','latex');
text(0.5*(t_scaled(ind_T(1)) + t_scaled(ind_T(end))), -0.2,'$T_f$','fontsize',fs,'HorizontalAlignment', 'center','Interpreter','latex');

strht = sprintf('$h_T = %.2f $m',armcrit);
strqt = sprintf('$Q_T = %.1f $m$^3$/s',QT);
strhm = sprintf('$h_m = %.2f $m',hm);
strqm = sprintf('$Q_m = %.1f $m$^3$/s',Qm);
strfev = sprintf('$FEV \\approx %.2f $Mm$^3$',armexcessvol*10^-6);
strtf = sprintf('$T_f = %.2f $hrs', Tf/3600);

str = {strfev,strtf,strht,strhm,strqt,strqm};

dim = [0.65,0.15,0.2,0.2];

tb = annotation('textbox',dim,'String',str,'Interpreter','latex');
tb.LineStyle = 'none';
tb.FitBoxToText = 'on';
tb.FontSize = fs;


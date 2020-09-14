%%% Plotting routine: FEV and sidelength as a function of threshold

%to export: 16x12cm

%% preamble
fs = 14;

%% Plot: 2 y axes
fig = figure(99);

yyaxis left
plot(armstep,armexcvol/10^6,'-','linewidth',2); hold on;
plot(armstep,armexcvol/10^6,'xk','linewidth',1); hold on;
axis([armstep(1) armstep(end) 0 ceil(max(armexcvol/10^6))]);
xlabel('$h_T$ [m]','fontsize',fs,'Interpreter','latex');
ylabel('$FEV$ [Mm$^3$]','fontsize',fs,'Interpreter','latex');

yyaxis right
plot(armstep,sqrt(armexcvol/2),'-','linewidth',2); hold on;
plot(armstep,sqrt(armexcvol/2),'ok','linewidth',1); hold on;
axis([armstep(1) armstep(end) 0 round(max(sqrt(armexcvol/2))+500, 1, 'significant')]);
ylabel('2m-deep lake side [m]','fontsize',fs,'Interpreter','latex');



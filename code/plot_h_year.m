%%  Plotting routine: flow data h=h(t) for whole year
% to export:  30x12 cm, fit to axes

%%
h_min = 0;
h_max = ceil(max(stage));

%%

fs = 12;
figure(101);
plot(timeh,stage,'-k','linewidth',2);

xlabel('$t$ [day]','fontsize',fs,'Interpreter','latex')
ylabel('$\bar{h}$ [m]','fontsize',fs,'Interpreter','latex');
axis([timeh(1) timeh(end) h_min h_max]);

ax = gca;
ax.YTick =  [0:1:h_max];
ax.YTickLabel = [0:1:h_max];

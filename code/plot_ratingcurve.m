%% plot rating curve with standard errors

fs = 14;
q_max = 0.5*round(2*max(rcdischarge)+50, 1, 'significant'); % round up to next multiple of 50
%%

figure(105);
% rating curve with limbs
plot(rcstage,rcdischarge,'k'); hold on;
plot([arml(1) arml(1)], [0 rcdischarge(end)],':k'); hold on;
plot([armu(1) armu(1)], [0 rcdischarge(end)],':k'); hold on;
plot([armu(2) armu(2)], [0 rcdischarge(end)],':k'); hold on;
plot([armu(3) armu(3)], [0 rcdischarge(end)],':k'); hold on;

% lower/upper curves
% plot(rcstage,rcdischargeL,'k'); hold on;
% plot(rcstage,rcdischargeU,'k'); hold on;
err = fill_between(rcstage, rcdischargeL, rcdischargeU); hold on;
err.FaceAlpha = 0.1;
err.EdgeColor = 'none';

text(arml(1),rcdischarge(end),'$h_0$','fontsize',fs,'Interpreter','latex','HorizontalAlignment', 'center');
text(armu(1),rcdischarge(end),'$h_1$','fontsize',fs,'Interpreter','latex','HorizontalAlignment', 'center');
text(armu(2),rcdischarge(end),'$h_2$','fontsize',fs,'Interpreter','latex','HorizontalAlignment', 'center');
text(armu(3),rcdischarge(end),'$h_3$','fontsize',fs,'Interpreter','latex','HorizontalAlignment', 'center');



%%
figure(106);
% Q = Q(t)
plot(t,q2,'k','Linewidth',1.5); hold on;

% Lower / upper bounds
% plot(t,dischargeL(ndecarmley(1):ndecarmley(2))); hold on;
% plot(t,dischargeU(ndecarmley(1):ndecarmley(2))); hold on;
err2 = fill_between(t, q2L, q2U); hold on;
err2.FaceAlpha = 0.1;
err2.EdgeColor = 'none';
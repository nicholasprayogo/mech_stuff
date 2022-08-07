% Filename: lab5i.m
% This file is executed by lab5.mdl during the Initialization stage.
% It can be used to initialize controller and other parameters.

% DO NOT CHANGE THE FOLLOWING CODE
%====================================================================
%====================================================================

% Weighting factors used by PD controller block
wp = [1.0; 1.0; 1.0];
wd = [1.0; 1.0; 1.0];

% Initial joint positions
q1_0 = 0.0;
q2_0 = 0.0;
q3_0 = -pi/2.0;

%====================================================================
%====================================================================

% m2 = 0.035; m3 = 0.1;
% L2 = 0.13335; Lc2 = 0.066675; Lc3 = 0.10668;
ml2 = 0.035; ml3 = 0.1;
l2 = 0.13335; lc2 = 0.066675; lc3 = 0.10668;

I1yy = 1.5e-4;
I2yy = 2.126e-4; I2zz = 2.126e-4;
I3yy = 6.075e-4; I3zz = 6.075e-4;
f = 1200.0;
I1yy = f*I1yy;
I2yy = f*I2yy;
I2zz = f*I2zz;
I3yy = f*I3yy;
I3zz = f*I3zz;

% Add your own code here
d11 = I1yy ;
d22 = ml2 * lc2^2 + I2zz + ml3*lc3^2 + ml3*l2^2 + I3zz;
d33 = ml3 * lc3^2 + I3zz ;
Dbar = diag([d11 d22 d33]);
PO = 10 ;
Ts = 2.5;

damping_ratio = - log(PO/100)/sqrt(pi^2 + log(PO/100)^2);
natural_freq = 4.6/(Ts*damping_ratio);
Z = diag([damping_ratio, damping_ratio, damping_ratio]);
Ohm = diag([natural_freq, natural_freq, natural_freq]);
   
% % no gravity compensation
% Kp = Dbar * Ohm.^2;
% Kd = 2 * Dbar * Z * Ohm;
% Kp = diag(Kp);
% Kd = diag(Kd);

% gravity compensation
g = 9.8;
G = diag([0 
    ,-ml2*g*cos(q2_0)*lc2 - g*ml3*lc3*cos(q2_0+q3_0) - g*ml3*cos(q2_0)*l2,
    -g*ml3*lc3*cos(q2_0+q3_0)]);
   
Kp = Dbar * Ohm.^2 - G;
Kd = 2 * Dbar * Z * Ohm;
Kp = diag(Kp);
Kd = diag(Kd);

Ax = 0.03;
Ay = 0.03;
Az = 0;
x0 = 0.15;
y0 =0;
z0 =0.035;

w0 = pi/4;

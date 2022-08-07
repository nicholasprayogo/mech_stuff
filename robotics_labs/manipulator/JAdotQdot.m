function JAdqd = JAdotQdot(q, qdot)

m2 = 0.035
m3 = 0.1
l2 = 0.13335
l3 = 0.13335
lc2 = 0.5 * l2
lc3 = 0.9 * l3
d1 = 0.168 

q1 = q(1);
q2 = q(2);
q3 = q(3);
q1d = qdot(1);
q2d = qdot(2);
q3d = qdot(3);

% Enter code for the J_A dot matrix here:

JAdot = [ -cos(q1)*(l3*cos(q2 + q3) + l2*cos(q2)),  sin(q1)*(l3*sin(q2 + q3) + l2*sin(q2)),  l3*sin(q2 + q3)*sin(q1);
 -sin(q1)*(l3*cos(q2 + q3) + l2*cos(q2)), -cos(q1)*(l3*sin(q2 + q3) + l2*sin(q2)), -l3*sin(q2 + q3)*cos(q1);
                                       0,                                       0,                        0]
% Determine: J_A dot times qdot

JAdqd = JAdot*qdot;

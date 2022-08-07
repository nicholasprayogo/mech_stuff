function p = for_kin(q)

import librobot.*

% dh(a_i, alpha_i, d_i, theta_i)
syms l2 l3 d1 q1 q2 q3; 

H10 = dh(0, pi/2, d1, q1);
H21 = dh(l2, 0, 0, q2);
H32 = dh(l3, 0, 0, q3);
H30 = simplify(H10*H21*H32);

l2 = 0.13335; 
l3 = 0.13335;
d1 = 0.168;

q1 = q(1);
q2 = q(2);
q3 = q(3);

H30_numeric = double(subs(H30));

% compute end-effector location [px; py; pz]
px = H30_numeric(1,4);
py = H30_numeric(2,4);
pz = H30_numeric(3,4);

p = [px; py; pz];



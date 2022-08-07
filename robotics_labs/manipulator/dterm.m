function Dv = dterm(q, v)

q1 = q(1); q2 = q(2); q3 = q(3);

ml2 = 0.035; ml3 = 0.1;
l2 = 0.13335; lc2 = 0.066675; lc3 = 0.10668;

I1yy = 0.18;
I2yy = 0.25512; I2zz = 0.25512;
I3yy = 0.729;   I3zz =0.729; 

% Fill in the elements of the D matrix below
D = [0,0,0;0,0,0;0,0,0];
D(1,1) = I1yy + I3yy*cos(q2 + q3)^2 + I2yy*cos(q2)^2 + ml3*cos(q1)^2*(lc3*cos(q2 + q3) + l2*cos(q2))^2 + ml3*sin(q1)^2*(lc3*cos(q2 + q3) + l2*cos(q2))^2 + lc2^2*ml2*cos(q1)^2*cos(q2)^2 + lc2^2*ml2*cos(q2)^2*sin(q1)^2;
D(1,2) = 0;
D(1,3) = 0;
D(2,1) = 0;
D(2,2) = I2zz + I3zz + l2^2*ml3 + lc2^2*ml2 + lc3^2*ml3 + 2*l2*lc3*ml3*cos(q3);
D(2,3) = I3zz + lc3^2*ml3 + l2*lc3*ml3*cos(q3);
D(3,1) = 0;
D(3,2) = I3zz + lc3^2*ml3 + l2*lc3*ml3*cos(q3);
D(3,3) = I3zz + lc3^2*ml3;

Dv = D*v;

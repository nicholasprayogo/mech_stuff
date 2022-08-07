function N = nterm(q, qdot)

% DO NOT CHANGE THE FOLLOWING CODE
%====================================================================
%====================================================================

% q1 to q3
q1 = q(1); q2 = q(2); q3 = q(3);

% q1 dot to q3 dot
q1dot = qdot(1); q2dot = qdot(2); q3dot = qdot(3);

% % Robot's physical parameters
% m2 = 0.035;  m3 = 0.1;
% L2 = 0.13335; L3 = L2;
% Lc2 = 0.5*L2;  Lc3 = 0.9*L3;
% 
% I1yy = 0.18;
% I2yy = 0.25512; I2zz = 0.25512;
% I3yy = 0.729;   I3zz =0.729; 

q1 = q(1); q2 = q(2); q3 = q(3);

ml2 = 0.035; ml3 = 0.1;
l2 = 0.13335; lc2 = 0.066675; lc3 = 0.10668;

I1yy = 0.18;
I2yy = 0.25512; I2zz = 0.25512;
I3yy = 0.729;   I3zz =0.729; 


% Friction coefficients
Fv11 = 1.0e-4; Fv22 = 1.0e-4; Fv33 = 1.0e-4;

%====================================================================
%====================================================================

g = 9.8;
% Add your own code here

% Set up the elements of the vector G
G1 = 0;
G2 = - g*lc3*ml3*cos(q2 + q3) - g*l2*ml3*cos(q2) - g*lc2*ml2*cos(q2);
G3 = -g*lc3*ml3*cos(q2 + q3);

% ch = [[0,0,0;0,0,0;0,0,0];
%     [0,0,0;0,0,0;0,0,0];
%     [0,0,0;0,0,0;0,0,0]]

ch = zeros(3,3,3);
ch(1,1,1) = 0;
ch(1,1,2) = - (I3yy*sin(2*q2 + 2*q3))/2 - (I2yy*sin(2*q2))/2 - (lc3^2*ml3*sin(2*q2 + 2*q3))/2 - (l2^2*ml3*sin(2*q2))/2 - (lc2^2*ml2*sin(2*q2))/2 - l2*lc3*ml3*sin(2*q2 + q3);
ch(1,1,3) = - (I3yy*sin(2*q2 + 2*q3))/2 - (lc3^2*ml3*sin(2*q2 + 2*q3))/2 - (l2*lc3*ml3*sin(q3))/2 - (l2*lc3*ml3*sin(2*q2 + q3))/2;
ch(1,2,1) = - (I3yy*sin(2*q2 + 2*q3))/2 - (I2yy*sin(2*q2))/2 - (lc3^2*ml3*sin(2*q2 + 2*q3))/2 - (l2^2*ml3*sin(2*q2))/2 - (lc2^2*ml2*sin(2*q2))/2 - l2*lc3*ml3*sin(2*q2 + q3);
ch(1,2,2) = 0;
ch(1,2,3) = 0;
ch(1,3,1) = - (I3yy*sin(2*q2 + 2*q3))/2 - (lc3^2*ml3*sin(2*q2 + 2*q3))/2 - (l2*lc3*ml3*sin(q3))/2 - (l2*lc3*ml3*sin(2*q2 + q3))/2;
ch(1,3,2) = 0;
ch(1,3,3) = 0;
ch(2,1,1) = (I3yy*sin(2*q2 + 2*q3))/2 + (I2yy*sin(2*q2))/2 + (lc3^2*ml3*sin(2*q2 + 2*q3))/2 + (l2^2*ml3*sin(2*q2))/2 + (lc2^2*ml2*sin(2*q2))/2 + l2*lc3*ml3*sin(2*q2 + q3);
ch(2,1,2) = 0;
ch(2,1,3) = 0;
ch(2,2,1) = 0;
ch(2,2,2) = 0;
ch(2,2,3) = -l2*lc3*ml3*sin(q3);
ch(2,3,1) = 0;
ch(2,3,2) = -l2*lc3*ml3*sin(q3);
ch(2,3,3) = -l2*lc3*ml3*sin(q3);
ch(3,1,1) = (I3yy*sin(2*q2 + 2*q3))/2 + (lc3^2*ml3*sin(2*q2 + 2*q3))/2 + (l2*lc3*ml3*sin(q3))/2 + (l2*lc3*ml3*sin(2*q2 + q3))/2;
ch(3,1,2) = 0;
ch(3,1,3) = 0;
ch(3,2,1) = 0;
ch(3,2,2) = l2*lc3*ml3*sin(q3);
ch(3,2,3) = 0;
ch(3,3,1) = 0;
ch(3,3,2) = 0;
ch(3,3,3) = 0;

% Set up the elements of the C(q, q dot) terms

% To get Cqqdot_i, fix the value of i, then 
% Cqqdot_i is (sum from j=1 to n (sum from k=1 to n) C_i,jk q_j_dot q_k_dot)

n = 3;

% set i = 1
i = 1;
Cqqdot1 = 0;
for j = 1:n
    for k = 1:n
        Cqqdot1 = ch(i,j,k) *qdot(j) *qdot(k) + Cqqdot1;
    end
end
     
i = 2;
Cqqdot2 = 0;
for j = 1:n
    for k = 1:n
        Cqqdot2=ch(i,j,k) * qdot(j) *qdot(k) + Cqqdot2;
    end
end

i = 3;
Cqqdot3 = 0;
for j = 1:n
    for k = 1:n
        Cqqdot3 =ch(i,j,k) * qdot(j) *qdot(k)  + Cqqdot3;
    end
end

% Cqqdot1 = 1
% Cqqdot2 = 1
% Cqqdot3 = 1
N = [Cqqdot1 + G1 + Fv11*q1dot;
     Cqqdot2 + G2 + Fv22*q2dot;
     Cqqdot3 + G3 + Fv33*q3dot];

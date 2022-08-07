% function JAiv = JAInvV(q, v)
import librobot.*
syms l2 l3 d1 q1 q2 q3 lc2 lc3 g; 

% q = [0.15, -0.15, 0.15]
% q1 = q(1);
% q2 = q(2);
% q3 = q(3);

H10 = dh(0, pi/2, d1, q1)
H21 = dh(l2, 0, 0, q2);
H32 = dh(l3, 0, 0, q3);

H20 = simplify(H10*H21);
H30 = simplify(H10*H21*H32);
% Enter code for J_A matrix here: 
p30 = H30(1:3, 4)

syms f(q1, q2, q3)
f(q1, q2, q3) = p30

% JA = [0,0,0;
%     0,0,0;
%     0,0,0];

JA = sym('JA', [3 3])


n = 3;
q = [q1, q2, q3];

for i = 1:n
    for j = 1:n
%         disp(diff(p30(i), q(j)))
        JA(i,j) = diff(p30(i), q(j));
    end
end 

JA = JA

JAdot  = diff(JA)
% JA = [];

% Determine: inverse of J_A times v

JAiv = inv(JA)*v;

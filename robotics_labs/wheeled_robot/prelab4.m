
syms R 
angle = pi/6
R_s2r = [cos(angle), sin(angle); -sin(angle), cos(angle)]

% define positions relative to s frame
p_os0_s = [0; -R]
p_os1_s = [-R; 0]
p_os2_s = [ -cos(pi/2-angle)*R; cos(angle)*R]
p_os3_s = [0; R]
p_os4_s = [cos(pi/2-angle)*R; cos(angle)*R]
p_os5_s = [R;0]

% use rotation matrix to transform from frame S to R
p_os0_r = R_s2r * p_os0_s
p_os1_r  = R_s2r * p_os1_s 
p_os2_r  = R_s2r * p_os2_s 
p_os3_r  = R_s2r * p_os3_s 
p_os4_r  = R_s2r * p_os4_s 
p_os5_r  = R_s2r * p_os5_s 


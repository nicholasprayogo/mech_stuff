from time import time
from math import sqrt, pi, sin, cos, atan2
from numpy import array, dot, zeros
from numpy.linalg import norm

from myRobot import *
import sys 
# Set up sampling period T_s and stopping time T_f
T_s = 0.02
T_f = 30

# Set up initial pose
x_0 = 0
y_0 = 0
theta_0 = 0

# Set up goal position
x_f = 1.3
y_f = 1.5

# Set up p_0 and p_f
p_0 = array([x_0, y_0, theta_0])
p_f = array([x_f, y_f, 0])

# Set up error tolerance
epsilon = sqrt( 2.0*(0.5/100.0)**2)

# set up d_free and d_min
d_min = 0.08
d_free = 1.25*d_min

# Set up controller gains
k_rho = 1.0
k_beta = -1.0
k_alpha = (2.0/pi)*k_rho - (5.0/3.0)*k_beta + 0.5

# Initialize vector pr_dot to be used for inverse kinematics
pr_dot = zeros(shape=(3,1))

# Initialize vector d for storing the sensor measurements d_i 
d = array([10.0, 10.0, 10.0, 10.0, 10.0, 10.0]).T

# Initialize a 6x3 matrix u_iR.  The vector u_i^R is assigned the ith column
# of this matrix.  See Eq. (4.6) in lab manual.
u_iR = zeros(shape=(3,6))

# Sensor frame location as per Table 4.1
R = 0.13
halfR = R/2.0
root3Rover2 = sqrt(3.0)*R/2.0

# Sensor frame location as per Table 4.1
sensor_loc = array([
   [-halfR, -root3Rover2, -(2.0/3.0)*pi],
   [-root3Rover2, halfR, (5/6)*pi],
   [0, R, 1/2*pi],
   [halfR, root3Rover2, 1/3*pi],
   [root3Rover2, halfR, 1/6*pi],
   [root3Rover2, -halfR, -1/6*pi]
])

# open a file to store robot pose for plotting later
f = open('pose.csv', 'w')

# Initial robot and other variables
robot = myRobot(T_s)

robot.initialize(theta_0)

H_R_Si_list = [] 
for i in range(0,6):
  q = sensor_loc[i]
  H_R_Si = robot.HMatrix(q)
  H_R_Si_list.append(H_R_Si)

H_R_Si_array = array(H_R_Si_list)

p = p_0
dp = p_f - p_0
rho = norm(dp[0:2])
goal_reached = False
elapsed_time = 0.0

# Set start time
start_time = time()


# Control loop
while ( (not goal_reached) and (elapsed_time < T_f) ):

    robot.get_readings_update()

    # save data to file for plotting
    f.write('%10.3e %10.3e % 10.3e %10.3e %10.3e\n' % (elapsed_time, p[0], p[1], p[2], rho))

    x = p[0]
    y = p[1]
    theta = p[2]

    # Use forward kinematics to get p_dot
    p_dot = robot.forward_kinematics(robot.angular_velocities, theta)

    # Determine angle alpha (remember to use atan2 instead of atan)
    alpha = atan2(y_f-y, x_f-x)-theta

    d_si_list = []
    d_accepted = []
    u_R_list = []
    d_R_list = []
    accepted_indices = []
    
    collision_exist = False
     
    # Get sensor measurements w.r.t. sensor frames
    for i in range(0,6):
       d_measured = robot.Vraw_to_distance(robot.ir_sensors_raw_values[i])
       d[i] = d_measured
       
       if d_measured <= d_min:
           collision_exist = True
    
    if collision_exist:
        for i in range(0,6):
           d_measured = robot.Vraw_to_distance(robot.ir_sensors_raw_values[i])

           # find collision free paths 
                      
           if d_measured > d_free:
               d_accepted.append(d_measured)
               accepted_indices.append(i)
           
           # convert this path to vector d_Si
           d_si= array([d_measured, 0, 1])
           
           # transform from Si to R frame
           d_R_i = dot(H_R_Si_array[i], d_si)
           d_R_list.append(d_R_i) 
        
        # calculated unit path vectors
        u_R_list = [d_R_i/norm(d_R_list) for d_R_i in d_R_list]
        d_T = sum(d_accepted)
        
        # calculate weighted sum of path vectors
        u_R = sum([d[i]/d_T*u_R_list[i] for i in accepted_indices]) 
              
        # transform R to base link frame
        H_0_R = robot.HMatrix(p)
        u_0 = dot(H_0_R, u_R)
        
        # set temporary goal 
        p_T = d_free* u_0 
        
        alpha_bar = atan2(p_T[1]- y, p_T[0]-x) - theta
        alpha = alpha_bar
        
        rho_bar = norm([p_T[1]- y, p_T[0]-x])
        rho = rho_bar 
        
    beta = -(theta + alpha)

    # Determine kinear and angular velocities of the robot body (v, w)
    # using the control law given in Eqs. (4.12) and (4.13)
    v = k_rho * rho
    w = k_alpha * alpha + k_beta * beta
    
    # Determine pr_dot (temporary velocity desired)
    pr_dot[0] = v * cos(theta)
    pr_dot[1] = v * sin(theta)
    pr_dot[2] = w

    # Now use Inverse Kinematics to determine wheel ref velocities
    wheel_ref_vel = robot.inverse_kinematics(pr_dot, theta)

    # Apply motor limits
    wheel_ref_vel = robot.motor_sat(wheel_ref_vel, 5.0*pi)

    # Execute motion
    robot.set_angular_velocities(wheel_ref_vel)

    # Odometry update
    p = p + p_dot*T_s

    # Replace calculated update for theta with measured value from IMU
    p[2]= robot.orientation

    # Check to see if goal is reached
    dp = p_f - p
    rho = norm(dp[0:2])
    goal_reached = ( rho <= epsilon)

    # time update
    elapsed_time = time() - start_time


print('ELPASED TIME = %s rho = %s' % (elapsed_time, rho))

# Either goal is reached or current_time > T_f
if goal_reached:
   print('Goal is reached, error norm is', rho)
else:
   print('Failed to reach goal, error norm is', rho)

robot.stop()
robot.close()

f.close()

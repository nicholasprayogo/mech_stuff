# Example Projects on Robot Control

Lab material and diagrams were provided by ELE 719 and ELE 819 course instructor (Dr. Yao-Chon (John) Chen) @ TMU.

## Wheeled Robot Control (from ELE719)

This lab project is about obstacle avoidanc and motion control of a 3-wheel-drive robot. The motion control involves using forward kinematics for computing the robot velocity based on the wheel velocities, and vice versa using inverse kinematics. Then, for obstacle avoidance, the system detects an obstacle if one of the IR sensor measurements is beyond a certain safe threshold, computes collision-free paths (vectors) towards temporary safe goals, and then bringing the robot back to the original goal once safe. 

<img src="assets/3wd_robot.png" alt="drawing" width="500"/>

## Manipulator Control (from ELE819)

Here, I was tasked to build an operational space inverse dynamics controller with feedback linearization. The system's ultimate goal is to compute the required joint torques based on the operational space (end-effector) reference trajectories.

First, the outer loop control variable u is made linear with respect to the operational space feedback variables using PD controller gains.  
<img src="assets/feedback_linear.png" alt="drawing" width="150"/>

Then, joint accelerations are related to the end effector acceleration based on the inverse analytical Jacobian.  
<img src="assets/inverse_dynamics.png" alt="drawing" width="200"/>

The output torque vector (Q), with the dynamics equation of a robotic manipulator is
<img src="assets/manipulator_dynamics.png" alt="drawing" width="200"/>

Thus, in terms of the end effector feedback and acceleration, accounting for the steps above, the output torque vector would be    
<img src="assets/output_torque.png" alt="drawing" width="300"/>

This can be represented as a block diagram as such:   
<img src="assets/block_diagram.png" alt="drawing" width="500"/>
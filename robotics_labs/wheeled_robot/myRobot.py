from math import sin, cos, exp, sqrt, pi
from numpy import array, dot
import numpy as np
from Robot3WD import Robot

class myRobot(Robot):
    def __init__(self, sampling_period, wheel_radius=None, L=None):
        Robot.__init__(self, sampling_period, wheel_radius, L)

    # --------------------------------------------------------------------------------------#
    # Pre-Lab work for Experiment 2                                                         #
    # --------------------------------------------------------------------------------------#
    def inverse_kinematics(self, p_dot, theta):
        L = self._L
        wheel_radius = self._wheel_radius
        # print(p_dot)
        phi_dot = np.dot(np.array([
    	[sin(theta), -cos(theta), -L],
    	[cos(pi/6 + theta), sin(pi/6+ theta), -L],
    	[-cos(pi/6-theta), sin(pi/6- theta), -L]
    	]) * 1/wheel_radius, p_dot)
        phi_dot = phi_dot.flatten()
        # print(phi_dot)
        return phi_dot

    def move_left(self, vx, theta):
        p_dot = array([-vx, 0.0, 0.0]).T
        phi_dot = self.inverse_kinematics(p_dot, theta)
        self.set_angular_velocities(phi_dot)

    def move_forward(self, vy, theta):
        p_dot = array([0.0, vy, 0.0]).T
        phi_dot = self.inverse_kinematics(p_dot, theta)
        self.set_angular_velocities(phi_dot)

    def move_backward(self, vy, theta):
        p_dot = array([0.0, -vy, 0.0]).T
        phi_dot = self.inverse_kinematics(p_dot, theta)
        self.set_angular_velocities(phi_dot)

    def move_right(self, vx, theta):
        p_dot = array([vx, 0.0, 0.0]).T
        phi_dot = self.inverse_kinematics(p_dot, theta)
        self.set_angular_velocities(phi_dot)

    def rotate_CCW(self, w, theta):
        p_dot = array([0.0, 0.0, w]).T
        phi_dot = self.inverse_kinematics(p_dot, theta)
        self.set_angular_velocities(phi_dot)

    def rotate_CW(self, w, theta):
        p_dot = array([0.0, 0.0, -w]).T
        phi_dot = self.inverse_kinematics(p_dot, theta)
        self.set_angular_velocities(phi_dot)
    # ... (Fill in rest of code here) ...


    # --------------------------------------------------------------------------------------#
    # Pre-Lab work for Experiment 3                                                         #
    # --------------------------------------------------------------------------------------#
    def forward_kinematics(self, wheel_angular_velocities, theta):
      L = self._L
      wheel_radius = self._wheel_radius
      p_dot = dot(array([
          [2*sin(theta), 2*cos(theta+pi/6), -2*sin(theta+pi/3)], 
          [-2*cos(theta), 2*cos(theta-pi/3), 2*cos(theta+pi/3)], 
          [-1/L, -1/L,-1/L]
          ])*wheel_radius/3,wheel_angular_velocities)
      return p_dot


    def motor_sat(self, wheel_angular_velocities, limit_value):
      wheel_angular_velocities_bar = np.zeros(3)

      for index, i in enumerate(wheel_angular_velocities_bar):
          if wheel_angular_velocities[index] < -limit_value:
              wheel_angular_velocities_bar[index] = -limit_value
          elif wheel_angular_velocities[index] >= -limit_value and wheel_angular_velocities[index] <= limit_value:
              wheel_angular_velocities_bar[index] = wheel_angular_velocities[index]
          elif wheel_angular_velocities[index] > limit_value:
              wheel_angular_velocities_bar[index] = limit_value
          else:
              raise Exception("Error")

      return wheel_angular_velocities_bar

----------------------------------------------------------#
    
    #Define the HMatrix function
    def HMatrix(self, q):
      H = array([[cos(q[0]), -sin(q[2]), q[0]], [sin(q[0]), cos(q[2]), q[1]], [0,0,1]])
      return H
    
    #Define the Vraw_to_distance function
    def Vraw_to_distance(self, Vraw):
      d = 0.62095 * exp(-0.05396*sqrt(Vraw))
      return d

#### end of myrobot.py ###

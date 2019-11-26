# code modified from https://github.com/PySEE/PyRankine

from seuif97 import *
import pandas as pd
import numpy as np

def modified_rankine(T1 ,T4, P1, P2, P3, P5, P6):
    # State 1 is superheated vapor at 8MPa, 480C.
    p1=8.0

    if T1:
        t1 = T1
        h1 = pt2h(p1,t1)
        s1 = pt2s(p1,t1)

    else:
        t1 = px2t(p1, 1)
        h1 = px2h(p1, 1)          # h1 = 2758.0    From table A-3  kj/kg
        s1 = px2s(p1, 1)

    # State 2 is fixed by p2 =2.0MPa and the specific entropy s2, which is the same as that of state 1
    p2= P2
    s2=s1
    h2 = ps2h(p2,s2)
    t2=ps2t(p2,s2)

    # State 3  is fixed by p2 =0.7MPa and the specific entropy s2, which is the same as that of state 1
    p3= P3
    s3=s1
    h3 = ps2h(p3,s3)
    t3=ps2t(p3,s3)

    # State 4 is superheated vapor at 0.7 MPa, 440C.
    p4 = p3
    t4 = T4
    h4 = pt2h(p4,t4)                                                                      # in kj/kg
    s4 =pt2s(p4,t4)

    # State 5 : p5 =0.3MPa and s5 = s4
    p5= P5
    s5=s4
    h5 =ps2h(p5,s5)
    t5=ps2t(p5,s5)

    # State 6: p6=0.008MPA, s6= s4
    p6= P6
    s6=s4
    h6 =ps2h(p6,s6)
    t6 =ps2t(p6,s6)

    # State 7 : p7=0.008MP Saturated water at the condenser exit
    p7= p6
    t7=px2t(p7,0)
    h7=px2h(p7,0)
    s7=px2s(p7,0)
    v7=px2v(p7,0)

    # State 8 : p8=0.3MP at the exit of the first pump
    p8= p5
    s8=s7
    h8=ps2h(p8,s8)
    t8=ps2t(p8,s8)

    # state 9 : The liquid leaving the open feedwater heater at is saturated liquid at 0.3 MPa
    p9=  p8
    t9=px2t(p9,0)
    h9=px2h(p9,0)
    s9=px2s(p9,0)

    # State 10 p=8.0Mpa, at the exit of the second pump,
    p10= p1
    s10=s9
    h10 =ps2h(p10,s10)
    t10 =ps2t(p10,s10)

    # State 11: the feedwater exiting the closed heater
    p11= p1
    t11= 220
    h11 = pt2h(p11,t11)                                                                      # in kj/kg
    s11 =pt2s(p11,t11)

    # State 12: the condensate leaving the closed heater is saturated at 2 MPa.
    p12= p9
    t12=px2t(p12,0)
    h12=px2h(p12,0)
    s12=px2s(p12,0)

    # State 13:  the fluid passing through the trap undergoes a throttling process
    p13= p9
    h13=h12
    s13=ph2s(p13,h13)
    t13=ph2t(p13,h13)

    df = pd.DataFrame(columns=["Temperature (C)","Pressure (MPa)","Enthalpy (kJ/kg)","Entropy (kJ/kg*K)"])

    df.loc[1] = t1,p1,h1,s1
    df.loc[2] = t2,p2,h2,s2
    df.loc[3] = t3,p3,h3,s3
    df.loc[4] = t4,p4,h4,s4
    df.loc[5] = t5,p5,h5,s5
    df.loc[6] = t6,p6,h6,s6
    df.loc[7] = t7,p7,h7,s7
    df.loc[8] = t8,p8,h8,s8
    df.loc[9] = t9,p9,h9,s9
    df.loc[10] = t10,p10,h10,s10
    df.loc[11] = t11,p11,h11,s11
    df.loc[12] = t12,p12,h12,s12
    df.loc[13] = t13,p13,h13,s13
    print(df)

    ydash = (h11-h10)/(h2-h12)                          # the fraction of the total flow diverted to the closed heater
    ydashdash = ((1-ydash)*h8+ydash*h13-h9)/(h8-h5)     # the fraction of the total flow diverted to the open heater
    print(ydash, ydashdash)
    # mdot = 113.37

    # Part(a)
    wt1dot = (h1-h2) + (1-ydash)*(h2-h3)                       # The work developed by the first turbine per unit of mass entering in kj/kg
    wt2dot = (1-ydash)*(h4-h5) + (1-ydash-ydashdash)*(h5-h6)   # The work developed by the second turbine per unit of mass in kj/kg

    wp1dot = (1-ydash-ydashdash)*(h8-h7)                # The work for the first pump per unit of mass in kj/kg
    wp2dot = h10-h9                                     # The work for the second pump per unit of mass in kj/kg

    qindot = (h1-h11) + (1-ydash)*(h4-h3)  # The total heat added expressed on the basis of a unit of mass entering the first   turbine

    eta = (wt1dot+wt2dot-wp1dot-wp2dot)/qindot  # thermal efficiency

    efficiency = 100*eta
    work_output = (wt1dot+wt2dot-wp1dot-wp2dot)*mdot
    # work_output = wt2dot*mdot

    return(efficiency, work_output)

def ideal_rankine(T1=None, P1=None,P2=None, irreversible=None):
    # x: steam quality

    # mdot = 113.37
    # power requirement: 4500 kwh

    # t1 = 295 # celsius
    # p1 = 8.0

    p1 = P1

    # superheated
    if T1!=None:
        t1 = T1
        h1 = pt2h(p1,t1)
        s1 = pt2s(p1,t1)

    else:
        t1 = px2t(p1, 1)
        h1 = px2h(p1, 1)          # h1 = 2758.0    From table A-3  kj/kg
        s1 = px2s(p1, 1)          # s1 = 5.7432    From table A-3  kj/kg.k
    # print("T1:{}, P1:{}, H1:{}, S1:{}".format(t1,p1,h1, s1))

    # State  2 ,p2=0.008
    p2 = P2 # in MPa

    # State 3 is saturated liquid
    p3 = p2
    t3 = px2t(p3, 0)
    h3 = px2h(p3, 0)  # kj/kg
    s3 = px2s(p3, 0)
    # print("T3:{}, P3:{}, H3:{}, S3:{}".format(t3,p3,h3, s3))

    # State 4
    p4 = p1

    if irreversible:
        # state 2
        s2s = s1
        h2s=ps2h(p2,s2s)
        t2s=ps2t(p2,s2s)

        etat_t=0.85
        h2=h1-etat_t*(h1-h2s)
        t2 =ph2t(p2,h2)
        s2 =ph2s(p2,h2)

        # state 4
        s4s=s3
        h4s =ps2h(p4,s4s)
        t4s =ps2t(p4,s4s)
        etat_p=0.85
        h4=h3+(h4s-h3)/etat_p
        t4 =ph2t(p4,h4)
        s4 =ph2s(p4,h4)

    else:
        # state 2
        s2 = s1
        t2 = ps2t(p2, s2)
        h2 = ps2h(p2, s2)

        # state 4
        s4 = s3
        t4 = ps2t(p4,s4)
        h4 = pt2h(p4, t4)
    # print("T2:{}, P2:{}, H2:{}, S2:{}".format(t2,p2,h2, s2))

    # print("T4:{}, P4:{}, H4:{}, S4:{}".format(t4,p4,h4, s4))
    # t4 = ps2h(p4, s4)

    # Part(a)
    # Mass and energy rate balances for control volumes
    # around the turbine and pump give, respectively
    df = pd.DataFrame(columns=["Temperature (C)","Pressure (MPa)","Enthalpy (kJ/kg)","Entropy (kJ/kg*K)"])

    df.loc[1] = t1,p1,h1,s1
    df.loc[2] = t2,p2,h2,s2
    df.loc[3] = t3,p3,h3,s3
    df.loc[4] = t4,p4,h4,s4

    # print(df)
    # turbine
    wtdot = h1 - h2
    # print("Power from turbine(kJ/kg): ", wtdot)
    # print("Power from turbine(kwh/kg): ", wtdot)
    # print("Power from turbine(kJ/s (kW)): ", wtdot*mdot)

    # pump
    wpdot = h4 - h3
    # print("Power into pump: ", wpdot)
    # print("net work", (wtdot-wpdot)*mdot)
    # The rate of heat transfer to the working fluid as it passes
    # through the boiler is determined using mass and energy rate balances as
    qindot = h1-h4
    print("Qin: ", qindot)
    Wcycledot = 25.0    # the net power output of the cycle in MW
    mdot = (Wcycledot*10**3)/(wtdot-wpdot)       # mass flow rate in kg/s

    # thermal efficiency
    eta = (wtdot-wpdot)/qindot
    efficiency = eta*100
    work_output = (wtdot-wpdot)*mdot
    return t1, efficiency, mdot, work_output

def reheat(T1=None, P1=None, P4= None, irreversible=None):
    p1 = P1

    # superheated
    if T1!=None:
        t1 = T1
        h1 = pt2h(p1,t1)
        s1 = pt2s(p1,t1)

    else:
        t1 = px2t(p1, 1)
        h1 = px2h(p1, 1)          # h1 = 2758.0    From table A-3  kj/kg
        s1 = px2s(p1, 1)          # s1 = 5.7432    From table A-3  kj/kg.k

    # State  2
    p2 = p1/4 # in MPa

    # state5 = [p2, px2t(p3,0), px2h(p3,0), px2s(p3,0)]
    # State 4
    p4 = P4

    if irreversible:
        # state 2
        s2s=s1
        h2s =ps2h(p2,s2s)
        etat1=0.85
        h2=h1-etat1*(h1-h2s)
        s2=ph2s(p2,h2)
        t2=ph2t(p2,h2)

        # state 3
        t3 = t1-20
        p3 = p2
        h3 =pt2h(p3,t3)
        s3 =pt2s(p3,t3)

        # state 4
        s4s=s3
        h4s =ps2h(p4,s4s)
        etat2=etat1
        h4=h3-etat2*(h3-h4s)
        s4 =ph2s(p4,h4)
        t4 =ph2t(p4,h4)

    else:
        # state 2
        s2 = s1
        t2 = ps2t(p2, s2)
        h2 = ps2h(p2, s2)

        # state 3
        t3 = t1-20
        p3 = p2
        h3 =pt2h(p3,t3)
        s3 =pt2s(p3,t3)

        # state 4
        s4 = s3
        t4 = ps2t(p4,s4)
        h4 = ps2h(p4, s4)

    p5 = p4
    t5 = px2t(p5, 0)
    h5 = px2h(p5, 0)  # kj/kg
    s5 = px2s(p5, 0)

    p6 = p1
    s6=s5
    h6 =ps2h(p6,s6)
    t6=ps2t(p6,s6)

    # Part(a)
    # Mass and energy rate balances for control volumes
    # around the turbine and pump give, respectively
    df = pd.DataFrame(columns=["Temperature (C)","Pressure (MPa)","Enthalpy (kJ/kg)","Entropy (kJ/kg*K)"])

    df.loc[1] = t1,p1,h1,s1
    df.loc[2] = t2,p2,h2,s2
    df.loc[3] = t3,p3,h3,s3
    df.loc[4] = t4,p4,h4,s4
    df.loc[5] = t5,p5,h5,s5
    df.loc[6] = t6,p6, h6,s6

    print(df)
    # turbine
    wtdot = (h1-h2)+(h3-h4)
    # print("Power from turbine(kJ/kg): ", wtdot)
    # print("Power from turbine(kwh/kg): ", wtdot)
    # print("Power from turbine(kJ/s (kW)): ", wtdot*mdot)

    # pump
    wpdot = (h6-h5)
    # print("Power into pump: ", wpdot)
    # print("net work", (wtdot-wpdot)*mdot)
    qindot = (h1-h6)+(h3-h2)
    print("Qin: ", qindot)
    Wcycledot = 25.0    # the net power output of the cycle in MW

    mdot = (Wcycledot*10**3)/((h1-h2)+(h3-h4)-(h6-h5))
    # thermal efficiency
    eta = (wtdot-wpdot)/(qindot)
    efficiency = eta*100
    work_output = (wtdot-wpdot)*mdot
    return t1, efficiency, mdot, work_output

#
# T1= 400
# print(" \n\n\nIdeal Basic Rankine\n")
# efficiency, work_output = ideal_turbine(T1)
# print("Efficiency: {}%, Work output: {} kW".format(efficiency, work_output))
#
# temp_ranges = [[295.06,280],
#             # [740,640]
#             ]
# t1_ranges = [400,740]
# t4_ranges = [280,700]
#
# print("Modified Rankine\n")
# for i in temp_ranges:
#     T1 = i[0]
#     T4 = i[1]
#
#     efficiency, work_output = calculate_efficiency(T1,T4)
#     print("Efficiency: {}%, Work output: {} kW".format(efficiency, work_output))

power_required = 1.25*15516
print("Power requirement: ", power_required)

grid_size = 20

params = {"T1":np.linspace(400,740,grid_size) , "T4":np.linspace(300,640,grid_size),"p_initial":np.linspace(8,12,grid_size),"p_final":np.flip(np.linspace(0.001,0.01,20))}

supercritical = False
mode = "reheat"

irreversible = True

placeholder1 = "supercritical" if supercritical else "no_supercritical"
placeholder2 = "irreversible" if irreversible else "no_irreversibility"

if mode=="ideal":
    ideal_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P2 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
    for i in range(grid_size):
        if supercritical:
            T1 = params["T1"][i]
        else:
            T1 = None
        P1 = params["p_initial"][i]
        P2 = params["p_final"][i]
        T1, efficiency, mdot , work_output = ideal_rankine( T1, P1,P2, irreversible=irreversible)
        ideal_df.loc[i] = [T1,P1,P2,efficiency,mdot, work_output]

    ideal_df = ideal_df.round(3)

    if supercritical:
        save_path = "ideal_rankine_{}_{}.csv".format(placeholder1, placeholder2)
    else:
        save_path = "ideal_rankine_{}_{}.csv".format(placeholder1, placeholder2)

    ideal_df.to_csv(save_path)

    print(ideal_df)

elif mode == "reheat":
    reheat_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P4 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
    for i in range(grid_size):
        if supercritical:
            T1 = params["T1"][i]

        else:
            T1 = None
        P1 = params["p_initial"][i]
        P4 = params["p_final"][i]
        T1, efficiency, mdot , work_output = reheat(T1=T1, P1=P1, P4= P4, irreversible=irreversible)
        reheat_df.loc[i] = [T1,P1,P4,efficiency,mdot, work_output]

    if supercritical:
        save_path = "reheat_{}_{}.csv".format(placeholder1, placeholder2)
    else:
        save_path = "reheat_{}_{}.csv".format(placeholder1, placeholder2)

    print(reheat_df)
    reheat_df.to_csv(save_path)
#
# else:
#     modified_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P2 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
#     for i in range(grid_size):
#         if supercritical:
#             T1 = params["T1"][i]
#         else:
#             T1 = None
#         P1 = params["p_initial"][i]
#         P2 = params["p_final"][i]
#         T1, efficiency, mdot , work_output = modified_rankine( T1, P1,P2)
#         ideal_df.loc[i] = [T1,P1,P2,efficiency,mdot, work_output]
#
#     modified_df = modified_df.round(3)
#
#     if supercritical:
#         save_path = "modified_rankine_supercritical.csv"
#     else:
#         save_path = "modified_rankine_no_supercritical.csv"
#
#     ideal_df.to_csv(save_path)

# code modified from https://github.com/PySEE/PyRankine

from cycles import *
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

supercritical = True
mode = "open_fwh"

irreversible = False

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


elif mode == "open_fwh":
    reheat_open_fwh_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P5 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
    for i in range(grid_size):
        if supercritical:
            T1 = params["T1"][i]

        else:
            T1 = None
        P1 = params["p_initial"][i]
        P5 = params["p_final"][i]
        T1, efficiency, mdot , work_output = open_fwh(T1=T1, P1=P1, P5= P5, irreversible=irreversible)
        reheat_open_fwh_df.loc[i] = [T1,P1,P5,efficiency,mdot, work_output]

    if supercritical:
        save_path = "reheat_open_fwh_{}_{}.csv".format(placeholder1, placeholder2)
    else:
        save_path = "reheat_open_fwh_{}_{}.csv".format(placeholder1, placeholder2)

    print(reheat_open_fwh_df)
    reheat_open_fwh_df.to_csv(save_path)

elif mode == "open_close_fwh":
    reheat_open_fwh_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P5 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
    for i in range(grid_size):
        if supercritical:
            T1 = params["T1"][i]

        else:
            T1 = None
        P1 = params["p_initial"][i]
        P5 = params["p_final"][i]
        T1, efficiency, mdot , work_output = open_fwh(T1=T1, P1=P1, P5= P5, irreversible=irreversible)
        reheat_open_fwh_df.loc[i] = [T1,P1,P5,efficiency,mdot, work_output]

    if supercritical:
        save_path = "reheat_open_fwh_{}_{}.csv".format(placeholder1, placeholder2)
    else:
        save_path = "reheat_open_fwh_{}_{}.csv".format(placeholder1, placeholder2)

    print(reheat_open_fwh_df)
    reheat_open_fwh_df.to_csv(save_path)

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

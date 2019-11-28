# code modified from https://github.com/PySEE/PyRankine

from cycles import *
import matplotlib.pyplot as plt
if __name__ == "__main__":
    power_required = 1.25*15516
    print("Power requirement: ", power_required)

    grid_size = 20

    params = {"T1":np.linspace(400,740,grid_size) , "T4":np.linspace(300,640,grid_size),"p_initial":np.linspace(8,12,grid_size),"p_final":np.flip(np.linspace(0.001,0.01,20))}

    params = {"T1":np.linspace(200,740,grid_size) , "T4":np.linspace(300,640,grid_size),"p_initial":np.linspace(12,12,grid_size),"p_final":np.flip(np.linspace(0.001,0.001,20))}
    modes = ["basic", "reheat", "open_fwh", "open_close_fwh"]

    supercritical = True
    # mode = "open_fwh_hx"
    irreversible = False

    placeholder1 = "supercritical" if supercritical else "no_supercritical"
    placeholder2 = "irreversible" if irreversible else "no_irreversibility"
    basic_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P2 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
    basic_df2 = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P2 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
    for i in range(grid_size):
        if supercritical:
            T1 = params["T1"][i]
        else:
            T1 = None
        P1 = params["p_initial"][i]
        P2 = params["p_final"][i]
        df, T1, efficiency, mdot , work_output = basic_rankine( T1, P1,P2, irreversible=False)
        basic_df.loc[i] = [T1,P1,P2,efficiency,mdot, work_output]

    for i in range(grid_size):
        if supercritical:
            T1 = params["T1"][i]
        else:
            T1 = None
        P1 = params["p_initial"][i]
        P2 = params["p_final"][i]
        df, T1, efficiency, mdot , work_output = basic_rankine( T1, P1,P2, irreversible=True)
        basic_df2.loc[i] = [T1,P1,P2,efficiency,mdot, work_output]

    basic_df = basic_df.round(3)
    basic_best_config_df = df.round(3)

    save_path = "performance_data_short/basic_temponly_{}_{}.csv".format(placeholder1, placeholder2)
    best_path = "states_data/basic_best_{}_{}.csv".format(placeholder1, placeholder2)

    basic_df.to_csv(save_path)
    x = basic_df["T1 (Celsius)"]
    y1 = basic_df["Efficiency (%)"]
    y2 = basic_df2["Efficiency (%)"]
    plt.plot(x,y1, label="Ideal", marker ='1')
    plt.plot(x,y2, label="85 % isentropic efficiency", marker = 'x')
    plt.xlabel("Temperature")
    plt.ylabel("Efficiency (%)")
    plt.legend()
    plt.savefig(fname="temp_plot.png")
    plt.show()
    basic_best_config_df.to_csv(best_path)
    print(basic_df)

    # for mode in modes:
        # for supercritical in [True,False]:
        #     for irreversible in [True, False]:
                # placeholder1 = "supercritical" if supercritical else "no_supercritical"
                # placeholder2 = "irreversible" if irreversible else "no_irreversibility"
        #
        #         if mode=="basic":
        #             basic_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P2 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
        #             for i in range(grid_size):
        #                 if supercritical:
        #                     T1 = params["T1"][i]
        #                 else:
        #                     T1 = None
        #                 P1 = params["p_initial"][i]
        #                 P2 = params["p_final"][i]
        #                 df, T1, efficiency, mdot , work_output = basic_rankine( T1, P1,P2, irreversible=irreversible)
        #                 basic_df.loc[i] = [T1,P1,P2,efficiency,mdot, work_output]
        #
        #             basic_df = basic_df.round(3)
        #             basic_best_config_df = df.round(3)
        #
        #             save_path = "performance_data_short/basic_{}_{}.csv".format(placeholder1, placeholder2)
        #             best_path = "states_data/basic_best_{}_{}.csv".format(placeholder1, placeholder2)
        #
        #             basic_df.to_csv(save_path)
        #             basic_best_config_df.to_csv(best_path)
        #             print(basic_df)
        #
        #         elif mode == "reheat":
        #             reheat_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P4 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
        #             for i in range(grid_size):
        #                 if supercritical:
        #                     T1 = params["T1"][i]
        #                 else:
        #                     T1 = None
        #                 P1 = params["p_initial"][i]
        #                 P4 = params["p_final"][i]
        #                 df, T1, efficiency, mdot , work_output = reheat(T1=T1, P1=P1, P4= P4, irreversible=irreversible)
        #                 reheat_df.loc[i] = [T1,P1,P4,efficiency,mdot, work_output]
        #
        #             reheat_df = reheat_df.round(3)
        #             reheat_best_config_df = df.round(3)
        #
        #             save_path = "performance_data_short/reheat_{}_{}.csv".format(placeholder1, placeholder2)
        #             best_path = "states_data/reheat_best_{}_{}.csv".format(placeholder1, placeholder2)
        #
        #             reheat_df.to_csv(save_path)
        #             reheat_best_config_df.to_csv(best_path)
        #             print(reheat_df)
        #
        #         elif mode == "open_fwh":
        #             reheat_open_fwh_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P5 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
        #             for i in range(grid_size):
        #                 if supercritical:
        #                     T1 = params["T1"][i]
        #                 else:
        #                     T1 = None
        #                 P1 = params["p_initial"][i]
        #                 P5 = params["p_final"][i]
        #                 df, T1, efficiency, mdot , work_output = open_fwh(T1=T1, P1=P1, P5= P5, irreversible=irreversible)
        #                 reheat_open_fwh_df.loc[i] = [T1,P1,P5,efficiency,mdot, work_output]
        #
        #             reheat_open_fwh_df = reheat_open_fwh_df.round(3)
        #             open_best_config_df = df.round(3)
        #
        #             save_path = "performance_data_short/reheat_open_fwh_{}_{}.csv".format(placeholder1, placeholder2)
        #             best_path = "states_data/reheat_open_fwh_best_{}_{}.csv".format(placeholder1, placeholder2)
        #
        #             print(reheat_open_fwh_df)
        #             reheat_open_fwh_df.to_csv(save_path)
        #             open_best_config_df.to_csv(best_path)
        #
        #         elif mode == "open_fwh_hx":
        #             reheat_open_fwh_hx_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P5 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
        #             for i in range(grid_size):
        #                 if supercritical:
        #                     T1 = params["T1"][i]
        #                 else:
        #                     T1 = None
        #                 P1 = params["p_initial"][i]
        #                 P5 = params["p_final"][i]
        #                 df, T1, efficiency, mdot , work_output = open_fwh_hx(T1=T1, P1=P1, P5= P5, irreversible=irreversible)
        #                 reheat_open_fwh_hx_df.loc[i] = [T1,P1,P5,efficiency,mdot, work_output]
        #
        #             reheat_open_fwh_hx_df = reheat_open_fwh_hx_df.round(3)
        #             open_hx_best_config_df = df.round(3)
        #
        #             save_path = "performance_data_short/reheat_open_fwh_hx_{}_{}.csv".format(placeholder1, placeholder2)
        #             best_path = "states_data/reheat_open_fwh_hx_best_{}_{}.csv".format(placeholder1, placeholder2)
        #
        #             print(reheat_open_fwh_hx_df)
        #             reheat_open_fwh_hx_df.to_csv(save_path)
        #             open_hx_best_config_df.to_csv(best_path)
        #
        #         elif mode == "open_close_fwh":
        #             open_close_fwh_df = pd.DataFrame(columns=['T1 (Celsius)','P1 (MPa)','P6 (MPa)', 'Efficiency (%)','Mass flow rate (kg/s)','Net Work (kW)'])
        #             for i in range(grid_size):
        #                 if supercritical:
        #                     T1 = params["T1"][i]
        #
        #                 else:
        #                     T1 = None
        #                 P1 = params["p_initial"][i]
        #                 P6 = params["p_final"][i]
        #                 df, T1, efficiency, mdot , work_output = open_close_fwh(T1=T1, P1=P1, P6= P6, irreversible=irreversible)
        #                 open_close_fwh_df.loc[i] = [T1,P1,P6,efficiency,mdot, work_output]
        #
        #             open_close_fwh_df = open_close_fwh_df.round(3)
        #             open_close_best_config_df = df.round(3)
        #
        #             save_path = "performance_data_short/reheat_open_close_fwh_{}_{}.csv".format(placeholder1, placeholder2)
        #             best_path = "states_data/reheat_open_close_fwh_best_{}_{}.csv".format(placeholder1, placeholder2)
        #
        #             print(open_close_fwh_df)
        #             open_close_fwh_df.to_csv(save_path)
        #             open_close_best_config_df.to_csv(best_path)

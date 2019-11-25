import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.ticker as ticker

dir_path = os.path.dirname(os.path.realpath(__file__))
measured = pd.read_csv(dir_path+"/measured_strain.csv")
deflection = pd.read_csv(dir_path+"/deflection.csv")
theoretical = pd.read_csv(dir_path+"/theoretical_strain.csv")
stress = pd.read_csv(dir_path+"/stress.csv")

indexers = [int(i) for i in range(1,6)]
loads = [42, 131, 274, 350, 448, 544]
gauge_locs = [0.5917, 0.3417, -0.1000, -0.7, -1.4083]

def stress_strain():
    for i in indexers:
        theoretical_vals = theoretical[" Strain {}".format(i)]
        measured_vals = measured[" Strain {}".format(i)]
        stress_vals = stress[" Stress {}".format(i)]

        plt.scatter(theoretical_vals, stress_vals, marker=".")
        plt.scatter(measured_vals, stress_vals, marker="+")
        # plt.autoscale(enable=True, axis="x")
        plt.xlabel("Strain")
        plt.ylabel("Stress (psi)")
        plt.title("Gauge {}".format(i))
        plt.legend(labels = ["Theoretical", "Measured"])
        plt.xlim(0.0, max(measured_vals))
        plt.ticklabel_format(axis="x", style="sci")
        plt.savefig(fname="gauge{}.png".format(i))
        plt.show()

def strain_distrib():

    for index, load in enumerate(loads):
        # print(measured.iloc[index][1:6])
        plt.plot(gauge_locs, measured.iloc[index][1:6], marker='o')
        plt.xticks(gauge_locs)
        plt.xlabel("Gauge distance from neutral axis (inches)")
        plt.ylabel("Strain")
        plt.title("Strain Distribution")
        # plt.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
        plt.ylim(0.0, max(measured.iloc[index][1:6])+0.0001)
        plt.legend(labels = [(str(i)+" lb") for i in loads])
    plt.show()

# strain_distrib()
def plot_deflection():
    plt.plot(loads, deflection["theoretical"], c="g", marker="o")
    plt.plot(loads, deflection["measured"], c = "r", marker ="o")
    plt.ylabel("Deflection (inches)")
    plt.xlabel("Load applied (lb)")
    plt.title("Deflection vs Load")
    plt.legend(labels=["Theoretical", "Measured"])
    plt.show()

plot_deflection()

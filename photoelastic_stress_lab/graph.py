import matplotlib.pyplot as plt
import pandas as pd

load8 = pd.read_csv("data/load8.csv")
load10 = pd.read_csv("data/load10.csv")
load12 = pd.read_csv("data/load12.csv")
load14 = pd.read_csv("data/load14.csv")

for index, load_data in enumerate([load8,load10,load12,load14]):
    x_null = load_data["null_order"]  # fringe location
    y_null = load_data["null_strain"]
    x_tardy = load_data["tardy_order"]
    y_tardy = load_data["tardy_strain"]

    plt.plot(x_null,y_null, label = 'Null', marker='1')
    plt.plot(x_tardy,y_tardy, label = 'Tardy', marker = '.')

    plt.xlabel("Corrected Fringe Order")
    plt.ylabel("Strain Difference")
    plt.legend()
    plt.show()

    plt.savefig(fname="load{}.png".format(8+index*2))

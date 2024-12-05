import matplotlib.pyplot as plt
import os
from constants import *


def save(fname):
    if DEV:
        return
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    # plt.savefig(f"./results/{fname}.pdf", dpi=DPI)
    # plt.savefig(f"./results/{fname}.svg", dpi=DPI)
    plt.savefig(f"./results/{fname}.png", dpi=DPI)
    plt.savefig(f"./results/{fname}.eps", format='eps', dpi=DPI)
    plt.savefig(f"./results/{fname}.pdf", format='pdf', dpi=DPI)
    print(f"INFO: Saved to {SAVE_PATH} with name {fname}")

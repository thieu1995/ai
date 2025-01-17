import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from model import script2
from pandas import read_csv

# pathsave = "/home/thieunv/Desktop/Link to LabThayMinh/code/6_google_trace/SVNCKH/testing/3m/sonia/result/cpu/"
# fullpath = "/home/thieunv/university/LabThayMinh/code/data/GoogleTrace/"

data = [3, 5, 8, 10]
list_number_data = [(11120, 13900, 0), (6640, 8300, 0), (4160, 5200, 0), (3280, 4100, 0)]


for i in range(0, len(data)):
    pathsave = "/home/hunter/nguyenthieu95/ai/6_google_trace/SVNCKH/script2/sonia/result/" + str(data[i]) + "m/ram/"
    fullpath = "/home/hunter/nguyenthieu95/ai/data/GoogleTrace/"
    filename = "data_resource_usage_" + str(data[i]) + "Minutes_6176858948.csv"
    df = read_csv(fullpath+ filename, header=None, index_col=False, usecols=[4], engine='python')
    dataset_original = df.values
    list_num = list_number_data[i]

    output_index = 0                # 0: cpu, 1: ram
    method_statistic = 0
    max_cluster=30
    mutation_id=1
    couple_activation = (2, 0)        # 0: elu, 1:relu, 2:tanh, 3:sigmoid

    epochs = [800, 1200, 2000]
    batch_sizes = [8, 32, 64]
    learning_rates = [0.05, 0.15, 0.35]
    sliding_windows = [ 2, 5]
    positive_numbers = [0.15]
    stimulation_levels = [0.20]
    distance_levels = [0.65]

    fig_id = 1
    so_vong_lap = 0
    for sliding in sliding_windows:
        for pos_number in positive_numbers:
            for sti_level in stimulation_levels:
                for dist_level in distance_levels:

                    for epoch in epochs:
                        for batch_size in batch_sizes:
                            for learning_rate in learning_rates:
                                if sliding == 5:
                                    sti_level = 0.45
                                para_data = {
                                    "dataset": dataset_original,
                                    "list_index": list_num,
                                    "output_index": output_index,
                                    "method_statistic": method_statistic,
                                    "sliding": sliding
                                }
                                para_net = {
                                    "epoch": epoch, "batch_size": batch_size, "learning_rate": learning_rate,
                                    "max_cluster": max_cluster, "pos_number": pos_number,
                                    "sti_level": sti_level, "dist_level": dist_level,
                                    "mutation_id": mutation_id, "couple_activation": couple_activation,
                                    "path_save": pathsave, "fig_id": fig_id
                                }

                                my_model = script2.SONIA(para_data, para_net)
                                my_model.fit()
                                so_vong_lap += 1
                                fig_id += 2
                                if so_vong_lap % 5000 == 0:
                                    print ("Vong lap thu : {0}".format(so_vong_lap))

    print ("Processing loop {0} DONE!!!".format(i))



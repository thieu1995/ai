import sys, os, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from model import script1
from model.utils import IOHelper
from pandas import read_csv
import tensorflow as tf

data = [10, 8, 5, 3]
list_number_data = [(3280, 4100, 0), (4160, 5200, 0), (6640, 8300, 0), (11120, 13900, 0)]

for i in range(0, len(data)):
    pathsave = os.path.dirname(os.path.abspath(__file__)) + "/result/" + str(data[i]) + "m/multi_cpu/"
    fullpath = os.path.abspath('../../data')
    filename = "/data_resource_usage_" + str(data[i]) + "Minutes_6176858948.csv"
    filesave_model = os.path.dirname(os.path.abspath(__file__)) + "/result/" + str(data[i]) + "m/multi_cpu.txt"

    df = read_csv(fullpath+ filename, header=None, index_col=False, usecols=[3, 4], engine='python')
    dataset_original = df.values
    list_num = list_number_data[i]

    output_index = 0                # 0: cpu, 1: ram
    method_statistic = 0
    max_cluster=50
    mutation_id=1
    couple_activation = (2, 0)        # 0: elu, 1:relu, 2:tanh, 3:sigmoid

    model = 0  # 0: sonia, 1: sobee

    epochs = [2000]
    batch_sizes = [32]
    learning_rates = [0.15]
    sliding_windows = [2, 3, 5]
    positive_numbers = [0.05, 0.15, 0.30]
    stimulation_levels = [0.20, 0.30, 0.40, 0.50, 0.6]
    distance_levels = [0.4, 0.55, 0.70]

    fig_id = 1
    so_vong_lap = 0
    for sliding in sliding_windows:
        for pos_number in positive_numbers:
            for sti_level in stimulation_levels:
                for dist_level in distance_levels:

                    for epoch in epochs:
                        for batch_size in batch_sizes:
                            for learning_rate in learning_rates:

                                start_time = time.time()
                                model_name = "_sliding=" + str(sliding) + "_posNumber=" + str(pos_number) +\
                                            "_stiLevel=" + str(sti_level) + "_disLevel=" + str(dist_level) + \
                                            "_epoch=" + str(epoch) + "_batchSize=" + str(batch_size) + "_learningRate=" + str(learning_rate)

                                para_data = {
                                    "dataset": dataset_original,
                                    "list_index": list_num,
                                    "output_index": output_index,
                                    "method_statistic": method_statistic,
                                    "sliding": sliding, "tf": tf
                                }
                                para_net = {
                                    "model": model, "epoch": epoch, "batch_size": batch_size, "learning_rate": learning_rate,
                                    "max_cluster": max_cluster, "pos_number": pos_number,
                                    "sti_level": sti_level, "dist_level": dist_level,
                                    "mutation_id": mutation_id, "couple_activation": couple_activation,
                                    "path_save": pathsave, "fig_id": fig_id, "model_name": model_name
                                }

                                my_model = script1.Model(para_data, para_net)
                                my_model.fit()
                                time_model = round(time.time() - start_time, 3)

                                temp = [my_model.time_cluster, my_model.time_train, time_model]
                                IOHelper.save_time(temp, my_model.RMSE, my_model.MAE, model_name, filesave_model)

                                so_vong_lap += 1
                                fig_id += 2
                                if so_vong_lap % 100 == 0:
                                    print ("Vong lap thu : {0}".format(so_vong_lap))

    print ("Processing loop {0} DONE!!!".format(i))



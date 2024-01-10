import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import json

def learning_curve_plot(history, run_folders):

    plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.axis([0, history.epoch[-1], 0, max(history.history['loss'] + history.history['val_loss'])])
    plt.legend(['loss', 'val_loss'], loc='upper right')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.savefig(run_folders["model_path"] + run_folders["exp_name"]+"/viz/"+"training_loss.png")
    plt.close()

def create_environment(run_folders):
    # Creating base folders
    try:
        os.mkdir(run_folders["model_path"])
    except:
        pass
    try:
        os.mkdir(run_folders["results_path"])
    except:
        pass

    # Preparing required I/O paths for each experiment
    if len(os.listdir(run_folders["model_path"])) == 0:
        exp_idx = 1
    else:
        exp_idx = len(os.listdir(run_folders["model_path"])) + 1

    exp_name = "exp_%04d" % exp_idx
    run_folders["exp_name"] = exp_name

    exp_model_folder = run_folders["model_path"] + run_folders["exp_name"] + '/'
    exp_res_model = run_folders["results_path"] + run_folders["exp_name"] + '/'

    try:
        os.mkdir(exp_model_folder)
    except:
        pass
    try:
        os.mkdir(exp_res_model)
    except:
        pass
    try:
        os.mkdir(os.path.join(exp_model_folder, 'viz'))
    except:
        pass
    try:
        os.mkdir(os.path.join(exp_model_folder, 'weights'))
    except:
        pass
    try:
        os.mkdir(os.path.join(exp_model_folder, 'images'))
    except:
        pass

# para guardar las imagenes generadas por el modelo
def save_reconstructed_images(y_true, y_pred, run_folders):
    for i in range(0, y_pred.shape[0]):
        original = (y_true[i] * 255).astype("uint8")
        recon = (y_pred[i] * 255).astype("uint8")
        output = np.hstack([original, recon])
        cv2.imwrite(run_folders["results_path"] + run_folders["exp_name"] + "/image_" + str(i) + ".png", output)

# se guardan los los hiperparametros en un json
def create_json(hyperparameters, run_folders):
    with open(run_folders["model_path"]+run_folders["exp_name"]+"/hyperparameters.json", 'w') as fp:
        json.dump(hyperparameters, fp)
#!/usr/bin/env python
# coding: utf-8

### Import libraries

import math
import os
import sys
import time

import numpy as np
import gym
import torch
import torch.multiprocessing as mp
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from PIL import Image
from torch.autograd import Variable

### Global variables

IN_COLAB = False
MODEL_PATH = 'breakout_a3c.pth'
ENV_NAME = os.getenv('ENV_NAME', 'BreakoutDeterministic-v4')
SEED = 22
NUM_PROCESSES = 4
EPISODES_TRAINING = 5000
EPISODES_TESTING = 5000
HEIGHT = 84
WIDTH = 84
N_FRAMES = 4
VALUE_LOSS_COEF = 0.5
GAMMA = 0.99
TRAINING_PARAMETERS = {
    'frames': N_FRAMES,
    'trajectory_steps': 64,
    'num_processes': NUM_PROCESSES
}


### Define model architecture

# Función para obtener la arquitectura del modelo actor-critic
# Nótese que tanto actor como critic comparten una etapa convolucional.
# Luego, la red se bifurca en dos salidad, una para el actor, y otra para el crític.
# El actor predice distribución de probabilidad de las acciones dado une stado.
# Sin embargo, en la arquitectura no aplicamos aún la activación softmax, lo haremos más adelante.
# De esta forma, podemos realizar operaciones más eficientes, como log_softmax, a partir de los logits.

class ActorCritic(nn.Module):
    def __init__(self):
        super(ActorCritic, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, 8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, 3, stride=1)

        self.fc1 = nn.Linear(7 * 7 * 64, 512)

        self.actor = nn.Linear(512, 4)  # number of actions
        self.critic = nn.Linear(512, 1) # linear output for value

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        
        # Flatten:
        x = x.view(-1, 7 * 7 * 64)

        x = F.relu(self.fc1(x))

        policy = self.actor(x)
        value = self.critic(x)

        return policy, value

# Función para traspasar los gradientes obtenidos en un proceso al modelo global
def ensure_shared_grads(model, shared_model):
    for param, shared_param in zip(model.parameters(),
                                   shared_model.parameters()):
        if shared_param.grad is not None:
            return
        shared_param._grad = param.grad


### Funciones para el pre-procesamiento observación-estado

# Función para pasar de rgb a gris, y re-escalar la imagen de entrada
def rgb2gray_and_resize(screen):
    # RGB a gris
    screen_grey = np.array(np.dot(screen[..., :3], [0.299, 0.587, 0.114]), dtype=np.uint8)
    img_from_arr = Image.fromarray(screen_grey)
    # Re-escalado
    img_from_arr = img_from_arr.resize((84, 84))

    return np.array(img_from_arr)

# Función para acoplar información temporal de frames pasados en el estado actual
def update_frame_sequence(state, obs, n_frames=4, width=84, height=84):
    
    # Escalado en intensidad de la observación
    obs = np.ascontiguousarray(rgb2gray_and_resize(obs), dtype=np.float32) / 255
    obs = torch.FloatTensor(obs)
    
    # Si es observación inicial, se repite el frame para tener consistencia en tamaño del ventanas del estado.
    if state is None:
        _state = obs.repeat(n_frames, 1).view(n_frames, width, height)
    # En caso contratio, se acopla la ultima observación al final del estado, quitando la imagen más antigua
    else:
        _state = state.view(n_frames, width, height)
        _state = torch.cat((_state[1:], obs.view((1, width, height))))

    return _state

### Funciones para el post-procesar la recompensa

def calculate_reward(reward):
    # Se realiza un clip de la recompensa para evitar valores muy altos en determinados entornos.
    reward = np.clip(1, -1, reward)

    return reward


### Funciones para el entrenamiento de un agente mediante A3C

def train(rank, episodes, training_params, shared_model, counter, lock, optimizer=None, models_path='models'):
    torch.manual_seed(SEED + rank)
    
    # Instancia un entorno y modelo para el proceso
    env = gym.make(ENV_NAME)
    model = ActorCritic()
    model.train()
    
    # Preparar optimizador. Es el encargado de actualizar los pesos tras obtener los gradientes.
    # Nótese que se le pasan los pesos del modelo global, que son los que se actualizan, no los del modelo local.
    optimizer = optim.Adam(shared_model.parameters(), lr=0.00025)
    
    # Inicializamos trayectoria y pre-procesamos de observación a estado
    obs = env.reset()
    state = None
    state = update_frame_sequence(state, obs, n_frames=training_params['frames'])
    
    
    ###################################
    ### Recopilamos trayectoria
    ###################################
    
    # Bucle de episodios de entrenamiento - en este caso, haremos una trayectoria por episodio
    for _ in range(int(episodes)):
        
        done = False
        # Buffer de memoria para ir acumulando values, acciones (probabilidades predichas), y recompensas
        values, log_probs, rewards  = [], [], []

        # Al inicito de la tratectoria, cogemos los pesos del último modelo global
        model.load_state_dict(shared_model.state_dict())

        # Recorremos la trayectoria - se acaba en el T definido, o al llegar al final.
        for step in range(training_params['trajectory_steps']):
            
            # Hacemos forward al actor-critic dado el estado actual
            logits, value = model(state.unsqueeze(0))
            
            # Obtenemos las probabilidades de la acción a partir de los logits  
            prob = F.softmax(logits, -1)
            # Obtenemos las log-probabilities, para posteriormente computar el gradiente de la policy
            log_prob = F.log_softmax(logits, -1)
            # Hacemos un muestreo de la acción a realizar a partir de las probabilidades
            action = prob.multinomial(num_samples=1)
            log_prob = log_prob.gather(1, Variable(action))
            
            # Con la acción seleccionada, se la pasamos al enviroment para obtener la recomensa y siguiente observación
            obs, reward, done, info = env.step(action.item())
            reward = calculate_reward(reward) # Post-procesamiento de la recompensa
            
            # Contador para tener trazabilidad del numero de steps realizados
            # Luego se usa por el agente de test para almacenar dicha variable
            with lock:
                counter.value += 1
            
            # Actualizamos el estado de la siguiente iteración a partir de la observación obtenida
            state = update_frame_sequence(state, obs, n_frames=training_params['frames'])
            
            # Almacenamiento de los value, log-probs y recompensa de la iteración para posteriormente computar los gradientes
            values.append(value)
            log_probs.append(log_prob)
            rewards.append(reward)
            
            # Si es estado terminal - reseteamos entorno y estado y salimos del bucle
            if done:
                obs = env.reset()
                state = None
                state = update_frame_sequence(state, obs, n_frames=training_params['frames'])
                break # Salimos del bucle de la trayectoria si es estado terminal

        ###################################
        ### Prepare for update the policy
        ###################################
        
        # Recompensa de estado final. Si es terminal, recompensa de 0. En caso contrario, estimamos con el value.
        R = torch.zeros(1, 1)
        if not done:
            _, value = model(state.unsqueeze(0))
            R = value.data
        values.append(Variable(R))
        
        policy_loss, value_loss  = 0, 0
        R = Variable(R) # Pasamos la recompensa a un tensor de pytorch.
        # Recorremos la trayectoria de forma inversa, calculando los criterios de optimización
        for i in reversed(range(len(rewards))):
            # 1. Obtener las discounted rewards para cada t
            R = GAMMA * R + rewards[i]
            # 2. Normalizar la recompensa mediante el value para obtener el advantadge
            advantage = R - values[i]
            
            # 3. Computo de criterio de optimización.
            # Nótese que se va acumulando los criterios a lo largo de la trayectoria
            
            # 3.1. Error cuadrático para el advantadge (advantage.pow(2)).
            # Con esto se optimiza la rama de la función critic. Recuerda, values[i] viene de dicha rama.
            value_loss = value_loss + advantage.pow(2)
            
            # 3.2. Gradientes de la policy (por eso lo ponemos en negativo) ponderados por el advantadge.
            # Ahora solo ponemos -log_prob, pero luego sacaremos los gradientes
            # Para evitar que se actualice el critic en este paso, creamos una nueva variable (Variable(advantage))
            policy_loss = policy_loss - (log_probs[i] * Variable(advantage))
        
        # Limpiamos gradientes del modelo global
        optimizer.zero_grad()
        # Función de pérdidas combinada. Con VALUE_LOSS_COEF le damos más importancia a la actualización de la policy
        loss_fn = (policy_loss + VALUE_LOSS_COEF * value_loss)
        # Con backward computamos los gradientes de los criterios computados anteriormente
        loss_fn.backward(retain_graph=True)
        # Pasamos los gradientes del modelo local al global
        ensure_shared_grads(model, shared_model)
        # Actualizamos los pasos en dirección de los gradientes
        optimizer.step()
        # Guardamos el modelo
        torch.save(shared_model.state_dict(), MODEL_PATH)

### Funciones para el testeo del agente

def test(rank, episodes, training_params, shared_model, counter, render=True, models_path='models'):
    torch.manual_seed(SEED + rank)

    env = gym.make(ENV_NAME)
    model = ActorCritic()
    model.eval()

    obs = env.reset()
    if (not IN_COLAB) and (render):
        obs = env.render(mode='rgb_array')
    state = None
    state = update_frame_sequence(state, obs, n_frames=training_params['frames'])

    rewards, reward_sum = [], 0
    value_acum, value_avg_best = [], -1000.0

    start_time = time.time()
    training_time = 0
    episode, episode_steps = 0, 0

    for _ in range(int(episodes)):
        model.load_state_dict(shared_model.state_dict())

        done = False
        while not done:
            logits, value = model(state.unsqueeze(0))
            prob = F.softmax(logits, -1)
            action = prob.multinomial(num_samples=1)

            obs, reward, done, info = env.step(action.item())
            if (not IN_COLAB) and (render):
                env.render()
            reward = calculate_reward(reward)

            episode_steps += 1
            rewards.append(reward)
            reward_sum += reward
            value_acum.append(value.data[0, 0])

            state = update_frame_sequence(state, obs, n_frames=training_params['frames'])

            if done:
                episode += 1
                episode_time = time.time() - start_time
                training_time += episode_time
                value_avg = np.mean(value_acum)

                if value_avg > value_avg_best:
                    torch.save(model.state_dict(), 'breakout_a3c_best.pth')
                    value_avg_best = value_avg

                dict_info = {}
                dict_info["episode"] = episode
                dict_info["episode_time_secs"] = (str(episode_time))
                dict_info["episode_steps"] = (str(episode_steps))
                dict_info["episode_reward"] = reward_sum
                dict_info["reward_min"] = np.min(rewards)
                dict_info["reward_max"] = np.max(rewards)
                dict_info["reward_avg_by_step"] = np.mean(rewards)
                dict_info["value_avg"] = value_avg
                dict_info["training_time"] = training_time
                dict_info["training_steps"] = (str(counter.value))

                print(dict_info)

                rewards, reward_sum = [], 0
                episode_steps = 0
                start_time = time.time()

                obs = env.reset()
                if (not IN_COLAB) and (render):
                    obs = env.render(mode='rgb_array')
                state = None
                state = update_frame_sequence(state, obs, n_frames=training_params['frames'])

                break


if __name__ == '__main__':
    torch.manual_seed(22)

    shared_model = ActorCritic()
    shared_model.share_memory()

    num_processes = int(TRAINING_PARAMETERS['num_processes'])
    processes = []

    counter = mp.Value('i', 0)
    lock = mp.Lock()

    print("Launching testing process")
    p = mp.Process(
        target=test,
        args=(num_processes, EPISODES_TESTING, TRAINING_PARAMETERS,
            shared_model, counter, lock, None))
    p.start()
    processes.append(p)

    print("Launching {} training processes".format(NUM_PROCESSES - 1))
    for rank in range(0, num_processes - 1):
        p = mp.Process(
            target=train,
            args=(rank, EPISODES_TRAINING, TRAINING_PARAMETERS, shared_model, counter, lock, None, None))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

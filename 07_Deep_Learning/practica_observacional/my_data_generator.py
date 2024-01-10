#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Imports necesarios
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image                                           # PARA CARGAR IMAGENES
from skimage.transform import resize                            # PARA TRANSFORMAR LA IMAGEN nn


# In[4]:

# SE CONSIGUE UN GENERADOR DE DATOS PROPIO
class DataGenerator(tf.keras.utils.Sequence):
    
    # EL CONSTRUCTOR 
    def __init__(self, data_frame, width, height, channels, batch_size=128, path_to_img="../data/images", shuffle=True):
        self.df = data_frame                                # CONTIENE LA INFO DEL CSV
        self.width = width                                  # EL ANCHO DE IMG
        self.height = height                                # EL ALTO DE LA IMG
        self.channels = channels                            # LOS CANALES
        self.batch_size = batch_size                        # TAMAÑO DEL BATCH
        self.path_to_img = path_to_img                      # LA UBICACIÓN DEL ARCHIVO
        self.shuffle = shuffle                              # MEZLAR 
        self.indexes = np.arange(len(data_frame.index))     # EL NÚMERO DE INDICES, UN ARRAY DE POSICIONES CON LA LONGITUD DEL DATAFRAME
    
    # DEVUELVE EL NÚMERO DEL BATCHES POR EPOCA # METODO PRIVADO
    def __len__(self):
        return int(np.ceil(len(self.indexes)/self.batch_size))
    
    # SE HACE UN SHUFFLE # METODO PUBLICO
    def on_epoch_end(self):
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
    
    # OBTENER UN BATCH A PARTIR DE UNA POSICION INDEX # METODO PRIVADO
    def __getitem__(self, index):
        '''
        Se recorren los datos de un indice al siguiente por el tamaño del batch, 
        se cogen tantas muestras como el tamaño del batch
        '''
        indexes = self.indexes[index*self.batch_size:(index + 1)*self.batch_size]
        
        #Inicializamos listas de datos
        X, Y = [], []
        
        for idx in indexes:                  # recorrere los indices
            x, y = self.get_sample(idx)      # la imagen y la etiqueta
            X.append(x)
            Y.append(y)
        return np.array(X), np.array(Y)
    
    # PARA LEER LA IMAGEN, Y PROCESARLA
    def get_sample(self, idx):
        df_row = self.df.iloc[idx]                                             # Se localiza la fila en el df
        image = Image.open(os.path.join(self.path_to_img, df_row["ImageID"]))  # se carge la imagen con un metodo de PLO
        image = image.resize((self.height, self.width))                        # se le da el tamaño deseado
        image = np.asarray(image)                                              # se pasa a un np array
        image2 = np.reshape(image, image.shape + (self.channels,))             # para generalizar a más canales segun el caso de uso
        #image2.setflags(write=1)
        image2 = self.norm(image2)                                             # se normaliza la imagen entre 0 y 1 y se pasa a np.float32
        label = image2
        return image2, label                                                   # devuelve la imagen procesada y la imagen original
    
    # PARA NORMALIZAR LAS IMAGENES CARGADAS
    def norm(self, image):
        image = image/255.0
        return image.astype(np.float32)


# In[ ]:





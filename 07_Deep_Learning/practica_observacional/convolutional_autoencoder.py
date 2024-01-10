#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tensorflow.keras.layers import Conv2D, Conv2DTranspose, BatchNormalization, LeakyReLU, Flatten, Lambda, Dense, Activation, Dropout, Reshape, Input
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, CSVLogger, EarlyStopping
from tensorflow.keras.utils import plot_model
from tensorflow.keras.optimizers import Adam
from utils import learning_curve_plot
from tensorflow.keras import backend as K
import numpy as np
import os
import pickle


# In[ ]:


class ConvAutoencoder:
    
    #CONSTRUCTOR
    def __init__(self, 
               input_dim,                # las diemsniones
               encoder_conv_filters,     # filtros encoder
               encoder_conv_kernels,     # el tamaño del kernel encoder 
               encoder_conv_strides,     # el stride enoder 
               decoder_conv_filters,     #
               decoder_conv_kernels,
               decoder_conv_strides,
               z_dim):
        self.input_dim = input_dim
        self.encoder_conv_filters = encoder_conv_filters
        self.encoder_conv_kernels = encoder_conv_kernels
        self.encoder_conv_strides = encoder_conv_strides
        self.decoder_conv_filters = decoder_conv_filters
        self.decoder_conv_kernels = decoder_conv_kernels
        self.decoder_conv_strides = decoder_conv_strides
        self.z_dim = z_dim
    
    # CREA LA ARQUITECTURA DEL MODELO
    def build(self, 
              use_batch_norm=False,      # por defecto no usara batch normalization
              use_dropout=False,         # por defecto no usara dropout
              VCAE=False):               # por defecto no usara Variacional auto encoder
        
        '''
        Primero define en encoder, luego el decoder, y 
        finalmente lo une todo.
        '''

        # CONSTRUIR EL ENCODER
        encoder_input = Input(shape=self.input_dim, name = 'encoder_input')  # Utiliza la API funcional
        x = encoder_input
        
        # PARA CADA CAPA CONVOLUCIONAL
        for i in range(len(self.encoder_conv_filters)):                      # crea la arquitectura con un bucle for
            conv_layer = Conv2D(filters=self.encoder_conv_filters[i],        # numero de filtros del bloque convolucional i 
                                kernel_size=self.encoder_conv_kernels[i],    # el tamaño del kernel del bloque convolucional i 
                                strides=self.encoder_conv_strides[i],        # el stride el bloque convolucional i 
                                padding='same',                              # por defecto 0 padding
                                name = 'encoder_conv'+str(i))                # le damos nombre
            x = conv_layer(x)                                                # se le indica a que capa esta unida en este caso a la anterior
            if use_batch_norm:                                               # si usamos batch normalization se lo aplica
                x = BatchNormalization()(x)
            
            x = LeakyReLU(alpha=0.2)(x)                                      # se aplica la función de activación se le indica la capa
            
            if use_dropout:                                                  # si se le indica el drop out se le añade
                x = Dropout(0.25)(x)
                
        shape_before_flattening = K.int_shape(x)[1:]                         # no se coge el tamaño del batch  
        x = Flatten()(x)                                                     # se le aplica el flatten
        encoder_output = Dense(self.z_dim, name='encoder_output')(x)         # este es el espacio latente
        
        # SE MAPEA EL ESPACIO LATENTE A UNA DISTRIVUCIÓN NOMRAL
        if VCAE:                                                             # Si el encoer fuera variacioanl
            self.mu = Dense(self.z_dim, name='mu')(x)                        # vector de medias
            self.log_var = Dense(self.z_dim, name='log_var')(x)              # vector de varianzas

            # SE CREA UNA FUNCIÓN DE MUESTREO
            def sampling(args):
                '''
                los args son el vector de media y varianza qeu definen la 
                distribucion normal multivariable, hay tantas variables como 
                dimensiones tenga el espacio latente
                '''
                mu, log_var = args
                epsilon = K.random_normal(shape=K.shape(mu), mean=0., stddev=1.)              # se crean las gaussianas
                return mu + K.exp(log_var/2)*epsilon
            
            # la salida del encoder es el mapeado del espacio latente a una N() multivarianza
            encoder_output = Lambda(sampling, name='encoder_ouput')([self.mu, self.log_var])
            
        self.encoder = Model(encoder_input, encoder_output)                 # se crea el ENCODER

        # SE CONTRUYE EL DECODER
        decoder_input = Input(shape=(self.z_dim,), name='decoder_input')    # la entrada del decoder 
        x = Dense(np.prod(shape_before_flattening))(decoder_input)          # pasar de la dimensionalidad z a la que teniamos antes del flatten
        x = Reshape(shape_before_flattening)(x)                             # ancho x alto x nº filtros antes del flatening
        
        for i in range(len(self.decoder_conv_filters)):                     # bucle for para las capas deconvolucionales
            conv_t_layer=Conv2DTranspose(filters=self.decoder_conv_filters[i], 
                                         kernel_size=self.decoder_conv_kernels[i], 
                                         strides=self.decoder_conv_strides[i], 
                                         padding='same',
                                         name='decoder_conv_t'+str(i))
            x = conv_t_layer(x)                                            # se une a la capa anterior
            
            if i<len(self.decoder_conv_filters)-1:                         # si no he llegado todavía al final de las convoluciones transpuestas
                x = LeakyReLU(alpha=0.2)(x)                                # añadele la función de activación
            else:
                x = Activation('sigmoid')(x)                               # si es la ultima capa se mapean los pixeles entre 0 y 1 como en la entrada
                
        decoder_output = x                                                 # se define el output
        self.decoder = Model(decoder_input, decoder_output)                # se crea el modelo DECODER: se pasa tanto la entrada como la salida
        
        # SE UNEN LAS DOS PARTES 
        #Creando el autoencoder convolucional
        autoencoder_input = encoder_input                                  
        autoencoder_output = self.decoder(encoder_output)                  # 
        autoencoder = Model(autoencoder_input, autoencoder_output)         # se unen las dos partes
        self.model = autoencoder                                           # se crea el atributo model como el AE completo
    
    # COMPILAMOS EL MODELO
    def compile(self, learning_rate=0.005, r_loss_factor=0.4, VCAE=False):
        self.learning_rate = learning_rate
        self.r_loss_factor = r_loss_factor
        optimizer = Adam(learning_rate=learning_rate) 

        # VARIACIONAL AUTO ENCODER
        if VCAE:

            # ERROR DE RECONSTRUCCIÓN
            def vae_r_loss(y_true, y_pred):                               
                r_loss = K.mean(K.square(y_true-y_pred), axis=[1,2,3])
                return r_loss * self.r_loss_factor                      # se multiplica la perdida por su factor de perdida
            
            # DIVERGENCIA DE KUBERT LEIBERT
            def vae_kl_loss(y_true, y_pred):
                kl_loss = -0.5 * K.sum(1 + self.log_var - K.square(self.mu) - K.exp(self.log_var), axis=1)
                return kl_loss
            
            # LA PERDIDA TOTAL DEL VAE ES LA SUMA DE LAS DOS ANTERIORES
            def vae_loss(y_true, y_pred):
                r_loss = vae_r_loss(y_true, y_pred)
                kl_loss = vae_kl_loss(y_true, y_pred)
                return r_loss + kl_loss
            
        # AUTO ENCODER
        else:
            self.model.compile(optimizer=optimizer, loss='mse')

    # METODO DE ENTRENAMIENTO      
    def train(self, 
              data_flow,                # flow de datos de entrenamiento
              epochs,                   # Numero de epocas
              steps_per_epoch,          # Numero de pasos
              data_flow_val,            # FLOW DE DATOS DE VALIDACIÓN
              run_folders):             # se almacenaran los resultados de entrenamiento
        
        csv_logger = CSVLogger(run_folders["log_filename"])
        checkpoint = ModelCheckpoint(os.path.join(run_folders["model_path"], 
                                                  run_folders["exp_name"]+'/weights/CAE_weights.h5'), 
                                                  save_weights_only=True,                               # salvar solo los pesos
                                                  verbose=1)                                            # para que escriba lo que hace
        
        lr_sched = self.step_decay_schedule(initial_lr=self.learning_rate, decay_factor=1, step_size=1) # caida del lr inicial 
        early_stop = EarlyStopping(monitor='val_loss', patience=25)                                     # para temprana para 25 epocas
        callbacks_list = [csv_logger, checkpoint, lr_sched, early_stop]                                 # se crea la lista de callbacks

        print("[INFO]: Training")
        history = self.model.fit(data_flow, 
                                 epochs=epochs, 
                                 validation_data=data_flow_val, 
                                 steps_per_epoch=steps_per_epoch, 
                                 callbacks=callbacks_list)
        self.save_model(run_folders, history)
    
    # reescribe la funcion de keras 
    def step_decay_schedule(self, initial_lr, decay_factor=1, step_size=1):
        def schedule(epoch):
            new_lr = initial_lr * (decay_factor ** np.floor(epoch/step_size))
            return new_lr
        return LearningRateScheduler(schedule)
    
    # función para guardar el modelo
    def save_model(self, run_folders, history):
        with open(os.path.join(run_folders["model_path"], run_folders["exp_name"]+'/CAE_model.pkl'), 'wb') as f:
            pickle.dump([self.input_dim
                        , self.encoder_conv_filters
                        , self.encoder_conv_kernels
                        , self.encoder_conv_strides
                        , self.decoder_conv_filters
                        , self.decoder_conv_kernels
                        , self.decoder_conv_strides
                        , self.z_dim], f)
        self.plot_model(run_folders)
        learning_curve_plot(history, run_folders)
    
    # METODO ESTATICO PARA CARGAR EL MODELO 
    @staticmethod
    def load_model(run_folders):
        with open(os.path.join(run_folders["model_path"], 
                               run_folders["exp_name"]+'/CAE_model.pkl'), 'rb') as f:
            params = pickle.load(f)
            
        my_CAE = ConvAutoencoder(*params)
        my_CAE.build(use_batch_norm=True, use_dropout=False, VCAE=False)
        my_CAE.model.load_weights(os.path.join(run_folders["model_path"], 
                                               run_folders["exp_name"]+'/weights/CAE_weights.h5'))
        return my_CAE
    
    # FUNCION PARA MOSTRAR LOS MODELOS
    def plot_model(self, run_folders):
        plot_model(self.model, to_file=os.path.join(run_folders["model_path"], run_folders["exp_name"]+'/viz/modelCAE.png'), show_shapes=True, show_layer_names=True)
        plot_model(self.encoder, to_file=os.path.join(run_folders["model_path"], run_folders["exp_name"]+'/viz/modelEncoder.png'), show_shapes=True, show_layer_names=True)
        plot_model(self.decoder, to_file=os.path.join(run_folders["model_path"], run_folders["exp_name"]+'/viz/modelDecoder.png'), show_shapes=True, show_layer_names=True)


# In[ ]:





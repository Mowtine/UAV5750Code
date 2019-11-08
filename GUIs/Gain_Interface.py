
# coding: utf-8

# In[1]:


import threading
from IPython.display import display, HTML
import ipywidgets as widgets
import time
import sys
from ipywidgets import Button, HBox, VBox, FloatSlider,Layout,Label,IntSlider, RadioButtons
import numpy as np
import socket
import pickle

#Gain names
names = ['Px', 'Ix', 'Dx', 'Ix_max', 'Ix_min',
         'Py', 'Iy', 'Dy', 'Iy_max', 'Iy_min',
         'Pz', 'Iz', 'Dz', 'Iz_max', 'Iz_min',
         'Pψ', 'Iψ', 'Dψ', 'Iψ_max', 'Iψ_min',
         'Pu', 'Iu', 'Du', 'Iu_max', 'Iu_min',
         'Pv', 'Iv', 'Dv', 'Iv_max', 'Iv_min',
         'Pw', 'Iw', 'Dw', 'Iw_max', 'Iw_min',
         'Pr', 'Ir', 'Dr', 'Ir_max', 'Ir_min']

max_int = 1000
min_der = -1.0
#Minimum value of each slider
min_val = [0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int,
          0, 0, min_der, 0,-max_int]

#Maximum value of each slider
max_val = [2, 2, 2, max_int,0,
           2, 2, 2, max_int,0,
           2, 2, 2, max_int,0,
           2, 2, 2, max_int,0,
           2, 2, 2, max_int,0,
           2, 2, 2, max_int,0,
           2, 2, 2, max_int,0,
           2, 2, 2, max_int,0]

#Initial value of each slider
init_val = [0, 0, 0, 0, 0,
           0, 0, 0, 0, 0,
           0, 0, 0, 0, 0,
           0, 0, 0, 0, 0,
           0.5, 0, 0, 0 ,0,
           0.5, 0, 0, 0, 0,
           0.5, 0, 0, 0, 0,
           0.5, 0, 0, 0, 0]

#make sliders and labels and combine
sliders = [FloatSlider(min=m,max=n,value=v,layout=Layout(flex='10 1 auto',width='auto', height='30px',margin='0 0 0 0')) 
         for m,n,v in zip(min_val,max_val,init_val)]
labels = [Label(w,layout=Layout(width='50',flex='0 0 auto')) for w in names]
items = [labels[int(i/2)] if i % 2 == 0 else sliders[int(i/2)] for i in range(2*len(labels))]

#TCP setup
TCP_IP = 'localhost'
TCP_PORT = 5006
BUFFER_SIZE = 1024

#Establish TCP communication 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

data_init=pickle.dumps(init_val)
conn.send(data_init)
print("init_data_sent")

#TuningGUI
out = VBox([HBox([w for w in items[i:i+10]]) for i in range(0,80,10)])
display(out)

#Input Switch
switch_label = Label('Input Option')
switch = RadioButtons(options=['RC Input', 'Onboard'])
display(HBox([switch_label,switch]))

#Controller Switch
switch_label = Label('Controller Option')
switch = RadioButtons(options=['manual','1-PID', '2-PID'])
display(HBox([switch_label,switch]))


def PIDLoop():
    
    t_start = time.time()
    prev_data = []
    
    while True :
        t_now = time.time()
        t = t_now - t_start
        
        # Get Gain Values from Tuning UI
        KP = [out.children[i].children[1].value for i in range(8)]
        KI = [out.children[i].children[3].value for i in range(8)]
        KD = [out.children[i].children[5].value for i in range(8)]
        Imax = [out.children[i].children[7].value for i in range(8)]
        Imin = [out.children[i].children[9].value for i in range(8)]

        #collect data
        data = [out.children[j].children[i].value for i in range(1,11,2) for j in range(8) ]
        switch_data = [switch.index]
        data.extend(switch_data)
        
        #send data when gain changed
        data_send=pickle.dumps(data)
        conn.send(data_send)
        prev_data = data
        
        try:
            time.sleep(0.01-(time.time()-t_now)) #designate frequency of the loop, 0.01s for example
        except:
            print('exec time more than 0.01')
################################################################################
                                #       Main Loop      #
################################################################################

# Load Tuning UI
thread = threading.Thread(target=PIDLoop)
thread.start()


# In[1]:


#stop this thread
thread.join()
s.close()
conn.close()


# In[ ]:


aaa = [1,1,1]
b = [2,2,2]
aaa==b


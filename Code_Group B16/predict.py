import sklearn
import pandas as pd
import numpy as np
import pickle

left = 1
middle = 2
right = 3

# position1 = dancer1 position
# position2 = dancer2 position
# position3 = dancer3 position
position1 = left
position2 = middle
position3 = right

def update_position(current_position):
  # input current_position and update dancers' position respectively
  global position1
  global position2
  global position3
  if (current_position == '1 2 3'):
    position1 = left
    position2 = middle
    position3 = right
  elif (current_position == '1 3 2'):
    position1 = left
    position2 = right
    position3 = middle
  elif (current_position == '2 1 3'):
    position1 = middle
    position2 = left
    position3 = right
  elif (current_position == '3 1 2'):
    position1 = middle
    position2 = right
    position3 = left
  elif (current_position == '2 3 1'):
    position1 = right
    position2 = left
    position3 = middle
  elif (current_position == '3 2 1'):
    position1 = right
    position2 = middle
    position3 = left

def return_output(): 
  global left
  global right
  global middle
  global position1
  global position2
  global position3

  if (position1 == left and position2 == middle and position3 == right):
    return '1 2 3'
  elif (position1 == left and position2 == right and position3 == middle):
    return '1 3 2'
  elif (position1 == middle and position2 == left and position3 == right):
    return '2 1 3'
  elif (position1 == middle and position2 == right and position3 == left):
    return '3 1 2'
  elif (position1 == right and position2 == left and position3 == middle):
    return '2 3 1'
  elif (position1 == right and position2 == middle and position3 == left):
    return '3 2 1'

def directioning(data):
  # check the last 5 datapoints to differentiate left or right
  count1 = 0
  count2 = 1
  length = len(data)
  test = data[length-4: length, 4]
  for x in test:
    if x < 0:
      count1 = count1 + 1 # right
    elif x > 0:
      count2 = count2 + 1 # left

  if count1 > count2:
    return False # right
  elif count2 > count1:
    return True # left

def positioning():
    global left
    global right
    global middle
    global position1
    global position2
    global position3
        
    dancer1 = pd.read_csv('input1.txt', skiprows=[i for i in range(10)], header=None).values
    len1 = len(dancer1)

    dancer2 = pd.read_csv('input2.txt', skiprows=[i for i in range(10)], header=None).values
    len2 = len(dancer2)

    dancer3 = pd.read_csv('input3.txt', skiprows=[i for i in range(10)], header=None).values
    len3 = len(dancer3)

    if len1 > 150:
        len1 = 4
    if len2 > 150:
        len2 = 4
    if len3 > 150:
        len3 = 4 
    
    if (len1 == 4 and len2 == 4 and len3 == 4): # all three do not move
      pass
    elif(len1 == 4): # dancer1 does not move
      temp = position2
      position2 = position3
      position3 = temp
    elif (len2 == 4): # dancer2 does not move
      temp = position1
      position1 = position3
      position3 = temp
    elif (len3 == 4): # dancer3 does not move
      temp = position1
      position1 = position2
      position2 = temp
    else: # all three moves
      if(len(dancer1) >= 50):
          direction1 = directioning(dancer1)
      if(len(dancer2) >= 50):
          direction2 = directioning(dancer2)
      if(len(dancer3) >= 50):
          direction3 = directioning(dancer3)
      if (position1 == left and position2 == middle and position3 == right): # 123
        if (direction2 == True): # dancer1 to right, dancer2 to left, dancer3 to left --> 231
          position1 = right
          position2 = left
          position3 = middle
        elif (direction2 == False): # dancer1 to right, dancer2 to right, dancer3 to left --> 312
          position3 = left
          position2 = right
          position1 = middle
      elif (position1 == left and position2 == right and position3 == middle): # 132
        if (direction3 == True): # dancer1 to right, dancer2 to left, dancer3 to left --> 321
          position1 = right
          position2 = middle
          position3 = left
        elif (direction3 == False): # dancer1 to right, dancer2 to left, dancer3 to right --> 213
          position3 = right
          position2 = left
          position1 = middle
      elif (position1 == middle and position2 == left and position3 == right): # 213
        if (direction1 == False): # dancer1 to right, dancer2 to right, dancer3 to left --> 321
          position1 = right
          position2 = middle
          position3 = left
        elif (direction1 == True): # dancer1 to left, dancer2 to right, dancer3 to left --> 132
          position3 = middle
          position2 = right
          position1 = left
      elif (position1 == middle and position2 == right and position3 == left): # 312
        if (direction1 == False): # dancer1 to right, dancer2 to left, dancer3 to right --> 231
          position1 = right
          position2 = left
          position3 = middle
        elif (direction1 == True): # dancer1 to left, dancer2 to left, dancer3 to right --> 123
          position3 = right
          position2 = middle
          position1 = left
      elif (position1 == right and position2 == left and position3 == middle): # 231
        if (direction3 == True): # dancer1 to left, dancer2 to right, dancer3 to left --> 312
          position1 = middle
          position2 = right
          position3 = left
        elif (direction3 == False): # dancer1 to left, dancer2 to right, dancer3 to right --> 123
          position3 = right
          position2 = middle
          position1 = left
      elif (position1 == right and position2 == middle and position3 == left): # 321
        if (direction2 == False): # dancer1 to left, dancer2 to right, dancer3 to right --> 132
          position1 = left
          position2 = right
          position3 = middle
        elif (direction2 == True): # dancer1 to left, dancer2 to left, dancer3 to right --> 213
          position3 = right
          position2 = left
          position1 = middle
    return return_output()

def bandpower(data, sf, band, method='welch', window_sec=None, relative=False):
    from scipy.signal import welch
    from scipy.integrate import simps

    band = np.asarray(band)
    low, high = band

    # Compute the modified periodogram (Welch)
    if method == 'welch':
        if window_sec is not None:
            nperseg = window_sec * sf
        else:
            nperseg = (2 / low) * sf

        freqs, psd = welch(data, sf, nperseg=nperseg)

    # Frequency resolution
    freq_res = freqs[1] - freqs[0]

    # Find index of band in frequency vector
    idx_band = np.logical_and(freqs >= low, freqs <= high)

    # Integral approximation of the spectrum using parabola (Simpson's rule)
    bp = simps(psd[idx_band], dx=freq_res)

    if relative:
        bp /= simps(psd, dx=freq_res)
    return bp


# calculate standard deviation of data in a given window size of 20 data points
def standard_deviation_binary(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.2)
  length = math.floor((length - window) / 1)
  std = [0] * length
  i = 0
  for x in range(length):
    std[x] = np.std(data[i:i+window])
    i = i + 1
  return std

# calculate mean absolute of data in a given window size of 20 data points
def mean_absolute_binary(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.2)
  length = math.floor((length - window) / 1)
  average = [0] * length
  i = 0
  for x in range(length):
    average[x] = abs(np.mean(data[i:i+window]))
    i = i + 1
  return average

# calculate variance of data in a given window size of 20 data points
def variance_binary(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.2)
  length = math.floor((length - window) / 1)
  var = [0] * length
  i = 0
  for x in range(length):
    var[x] = np.var(data[i:i+window])
    i = i + 1
  return var

# calculate bandpower of data in a given window size of 20 data points
def subbandpower_binary(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.2)
  length = math.floor((length - window) / 1)
  sbp = [0] * length
  i = 0
  for x in range(length):
    sbp[x] = bandpower(data[i:i+window], sf, [1, 20], 'welch')
    i = i + 1
  return sbp

# calculate max power spectral density of data in a given window size of 20 data points
def max_psd_binary(data, length):
  from scipy import signal
  import numpy as np
  import math
  sf = 200
  win = 0.5 * sf
  window = int(sf * 0.2)
  length = math.floor((length - window) / 1)
  psd_max = [0] * length
  i = 0

  for x in range(length):
    freq, psd = signal.welch(data[i:i+window], sf, nperseg = win)
    
    # remove low frequency component (f < 1 Hz)
    for j in range(len(freq)):
      if freq[j] < 1:
        psd[j] = 0

    psd_max[x] = abs(np.max(psd))
    i = i + 1
  
  return psd_max

def data_preprocessing_binary(action): 
  import pandas as pd
  import numpy as np
  from sklearn.preprocessing import StandardScaler
  import math

  accx = action[:,0]
  accy = action[:,1]
  accz = action[:,2]
  anglex = action[:,3]
  angley = action[:,4]
  anglez = action[:,5] 

  x_acc_std = []
  x_acc_mean = []
  x_acc_var = []
  x_acc_bp = []
  x_acc_psd = []

  y_acc_std = []
  y_acc_mean = []
  y_acc_var = []
  y_acc_bp = []
  y_acc_psd = []

  z_acc_std = []
  z_acc_mean = []
  z_acc_var = []
  z_acc_bp = []
  z_acc_psd = []

  x_angle_std = []
  x_angle_mean = []
  x_angle_var = []
  x_angle_bp = []
  x_angle_psd = []

  y_angle_std = []
  y_angle_mean = []
  y_angle_var = []
  y_angle_bp = []
  y_angle_psd = []

  z_angle_std = []
  z_angle_mean = []
  z_angle_var = []
  z_angle_bp = []
  z_angle_psd = []

  x_acc_std.extend(standard_deviation_binary(accx, len(accx)))
  x_acc_mean.extend(mean_absolute_binary(accx, len(accx)))
  x_acc_var.extend(variance_binary(accx, len(accx)))
  x_acc_bp.extend(subbandpower_binary(accx, len(accx)))
  x_acc_psd.extend(max_psd_binary(accx, len(accx)))

  y_acc_std.extend(standard_deviation_binary(accy, len(accy)))
  y_acc_mean.extend(mean_absolute_binary(accy, len(accy)))
  y_acc_var.extend(variance_binary(accy, len(accy)))
  y_acc_bp.extend(subbandpower_binary(accy, len(accy)))
  y_acc_psd.extend(max_psd_binary(accy, len(accy)))

  z_acc_std.extend(standard_deviation_binary(accz, len(accz)))
  z_acc_mean.extend(mean_absolute_binary(accz, len(accz)))
  z_acc_var.extend(variance_binary(accz, len(accz)))
  z_acc_bp.extend(subbandpower_binary(accz, len(accz)))
  z_acc_psd.extend(max_psd_binary(accz, len(accz)))

  x_angle_std.extend(standard_deviation_binary(anglex, len(anglex)))
  x_angle_mean.extend(mean_absolute_binary(anglex, len(anglex)))
  x_angle_var.extend(variance_binary(anglex, len(anglex)))
  x_angle_bp.extend(subbandpower_binary(anglex, len(anglex)))
  x_angle_psd.extend(max_psd_binary(anglex, len(anglex)))

  y_angle_std.extend(standard_deviation_binary(angley, len(angley)))
  y_angle_mean.extend(mean_absolute_binary(angley, len(angley)))
  y_angle_var.extend(variance_binary(angley, len(angley)))
  y_angle_bp.extend(subbandpower_binary(angley, len(angley)))
  y_angle_psd.extend(max_psd_binary(angley, len(angley)))

  z_angle_std.extend(standard_deviation_binary(anglez, len(anglez)))
  z_angle_mean.extend(mean_absolute_binary(anglez, len(anglez)))
  z_angle_var.extend(variance_binary(anglez, len(anglez)))
  z_angle_bp.extend(subbandpower_binary(anglez, len(anglez)))
  z_angle_psd.extend(max_psd_binary(anglez, len(anglez)))

  data = np.column_stack((x_acc_std, y_acc_std, z_acc_std, x_angle_std, y_angle_std, z_angle_std, x_acc_mean, y_acc_mean, z_acc_mean, x_angle_mean, y_angle_mean, z_angle_mean, x_acc_var, y_acc_var, z_acc_var, x_angle_var, y_angle_var, z_angle_var, x_acc_bp, y_acc_bp, z_acc_bp, x_angle_bp, y_angle_bp, z_angle_bp, x_acc_psd, y_acc_psd, z_acc_psd, x_angle_psd, y_angle_psd, z_angle_psd))

  return data

# calculate standard deviation of data in a given window size of 60 data points
def standard_deviation(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.3)
  length = math.floor((length - window) / 1)
  std = [0] * length
  i = 0
  for x in range(length):
    std[x] = np.std(data[i:i+window])
    i = i + 1
  return std

# calculate mean absolute of data in a given window size of 60 data points
def mean_absolute(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.3)
  length = math.floor((length - window) / 1)
  average = [0] * length
  i = 0
  for x in range(length):
    average[x] = abs(np.mean(data[i:i+window]))
    i = i + 1
  return average

# calculate variance of data in a given window size of 60 data points
def variance(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.3)
  length = math.floor((length - window) / 1)
  var = [0] * length
  i = 0
  for x in range(length):
    var[x] = np.var(data[i:i+window])
    i = i + 1
  return var

# calculate bandpower of data in a given window size of 60 data points
def subbandpower(data, length):
  import math
  import numpy as np
  sf = 200
  window = int(sf * 0.3)
  length = math.floor((length - window) / 1)
  sbp = [0] * length
  i = 0
  for x in range(length):
    sbp[x] = bandpower(data[i:i+window], sf, [1, 20], 'welch')
    i = i + 1
  return sbp

# calculate max power spectral density of data in a given window size of 60 data points
def max_psd(data, length):
  from scipy import signal
  import numpy as np
  import math
  sf = 200
  win = 0.5 * sf
  window = int(sf * 0.3)
  length = math.floor((length - window) / 1)
  psd_max = [0] * length
  i = 0

  for x in range(length):
    freq, psd = signal.welch(data[i:i+window], sf, nperseg = win)
    
    # remove low frequency component (f < 1 Hz)
    for j in range(len(freq)):
      if freq[j] < 1:
        psd[j] = 0

    psd_max[x] = abs(np.max(psd))
    i = i + 1
  
  return psd_max

def data_preprocessing(action): 
  import pandas as pd
  import numpy as np
  import math

  accx = action[:,0]
  accy = action[:,1]
  accz = action[:,2]
  anglex = action[:,3]
  angley = action[:,4]
  anglez = action[:,5] 

  x_acc_std = []
  x_acc_mean = []
  x_acc_var = []
  x_acc_bp = []
  x_acc_psd = []

  y_acc_std = []
  y_acc_mean = []
  y_acc_var = []
  y_acc_bp = []
  y_acc_psd = []

  z_acc_std = []
  z_acc_mean = []
  z_acc_var = []
  z_acc_bp = []
  z_acc_psd = []

  x_angle_std = []
  x_angle_mean = []
  x_angle_var = []
  x_angle_bp = []
  x_angle_psd = []

  y_angle_std = []
  y_angle_mean = []
  y_angle_var = []
  y_angle_bp = []
  y_angle_psd = []

  z_angle_std = []
  z_angle_mean = []
  z_angle_var = []
  z_angle_bp = []
  z_angle_psd = []

  x_acc_std.extend(standard_deviation(accx, len(accx)))
  x_acc_mean.extend(mean_absolute(accx, len(accx)))
  x_acc_var.extend(variance(accx, len(accx)))
  x_acc_bp.extend(subbandpower(accx, len(accx)))
  x_acc_psd.extend(max_psd(accx, len(accx)))

  y_acc_std.extend(standard_deviation(accy, len(accy)))
  y_acc_mean.extend(mean_absolute(accy, len(accy)))
  y_acc_var.extend(variance(accy, len(accy)))
  y_acc_bp.extend(subbandpower(accy, len(accy)))
  y_acc_psd.extend(max_psd(accy, len(accy)))

  z_acc_std.extend(standard_deviation(accz, len(accz)))
  z_acc_mean.extend(mean_absolute(accz, len(accz)))
  z_acc_var.extend(variance(accz, len(accz)))
  z_acc_bp.extend(subbandpower(accz, len(accz)))
  z_acc_psd.extend(max_psd(accz, len(accz)))

  x_angle_std.extend(standard_deviation(anglex, len(anglex)))
  x_angle_mean.extend(mean_absolute(anglex, len(anglex)))
  x_angle_var.extend(variance(anglex, len(anglex)))
  x_angle_bp.extend(subbandpower(anglex, len(anglex)))
  x_angle_psd.extend(max_psd(anglex, len(anglex)))

  y_angle_std.extend(standard_deviation(angley, len(angley)))
  y_angle_mean.extend(mean_absolute(angley, len(angley)))
  y_angle_var.extend(variance(angley, len(angley)))
  y_angle_bp.extend(subbandpower(angley, len(angley)))
  y_angle_psd.extend(max_psd(angley, len(angley)))

  z_angle_std.extend(standard_deviation(anglez, len(anglez)))
  z_angle_mean.extend(mean_absolute(anglez, len(anglez)))
  z_angle_var.extend(variance(anglez, len(anglez)))
  z_angle_bp.extend(subbandpower(anglez, len(anglez)))
  z_angle_psd.extend(max_psd(anglez, len(anglez)))

  data = np.column_stack((x_acc_std, y_acc_std, z_acc_std, x_angle_std, y_angle_std, z_angle_std, x_acc_mean, y_acc_mean, z_acc_mean, x_angle_mean, y_angle_mean, z_angle_mean, x_acc_var, y_acc_var, z_acc_var, x_angle_var, y_angle_var, z_angle_var, x_acc_bp, y_acc_bp, z_acc_bp, x_angle_bp, y_angle_bp, z_angle_bp, x_acc_psd, y_acc_psd, z_acc_psd, x_angle_psd, y_angle_psd, z_angle_psd))

  return data

label = ['cowboy', 'dab', 'logout', 'jamesbond', 'mermaid', 'pushback', 'scarecrow', 'snake', 'window360']

from pynq import (allocate, Overlay)

np.set_printoptions(suppress=True)

ol = Overlay('mlp.bit')

dma = ol.axi_dma_0
l1 = ol.layer1_accel_0 
l2 = ol.layer2_accel_0 
l3 = ol.layer3_accel_0 
l4 = ol.layer4_accel_0 

DIM1 = 30 #input layer
DIM2 = 9  #output layer
input_buffer = allocate(shape=(DIM1,), dtype=np.float32)
output_buffer = allocate(shape=(DIM2,), dtype=np.float32)

CTRL_REG = 0x00
AP_START = (1<<0) # bit 0
AUTO_RESTART = (1<<7) # bit 7

def run_kernel():
    dma.sendchannel.transfer(input_buffer)
    dma.recvchannel.transfer(output_buffer)
    l1.write(CTRL_REG, (AP_START | AUTO_RESTART)) #initialise layers
    l2.write(CTRL_REG, (AP_START | AUTO_RESTART))
    l3.write(CTRL_REG, (AP_START | AUTO_RESTART))
    l4.write(CTRL_REG, (AP_START | AUTO_RESTART))
    dma.sendchannel.wait()
    dma.recvchannel.wait()

def run_predict(test):
    count = {'cowboy':0, 'mermaid':0, 'dab':0, 'jamesbond':0, 'logout':0, 'pushback':0, 'scarecrow':0, 'snake':0, 'window360':0}

    for i in range(len(test)):
        for j in range(DIM1):
                input_buffer[j] = test[i][j]
        run_kernel()
        count[label[np.argmax(output_buffer)]] += 1
    return max(count, key=count.get)

def dance_or_position(test):
  # return dancing or positioning based on the data input
  loaded_model = pickle.load(open('dancing_positioning.sav', 'rb'))
  test = test[0:45, :]
  data = data_preprocessing_binary(test)
  ynew = loaded_model.predict(data)

  count1 = 0
  count2 = 0
  for x in ynew:
    if x == 'dancing':
      count1 = count1 + 1
    elif x == 'movement':
      count2 = count2 + 1

  if count1 > count2:
    return 'dancing'
  else:
    return 'positioning'

import pandas.io.common
from time import sleep

def main():
    moveType_1 = 'nil'
    moveType_2 = 'nil'
    moveType_3 = 'nil'
    
    old_data_1 = []
    old_data_2 = []
    old_data_3 = []
    
    old_data1 = []
    old_data2 = []
    old_data3 = []
    
    len1 = 0
    len2 = 0
    len3 = 0
    old1 = -1
    old2 = -1
    old3 = -1
    
    file = open("output.txt","w")
    file.close()
    file = open("positions.txt","w")
    file.close()
    file = open("input1.txt","w")
    file.write("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1")
    file.close()
    file = open("input2.txt","w")
    file.write("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1")
    file.close()
    file = open("input3.txt","w")
    file.write("1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1\n1")
    file.close()

    output_p = '1 2 3'

    isPredicted_1 = False
    isPredicted_2 = False
    isPredicted_3 = False
    done1 = False
    done2 = False
    done3 = False
    isMove = False
    
    count = {'cowboy':0, 'mermaid':0, 'dab':0, 'jamesbond':0, 'logout':0, 'pushback':0, 'scarecrow':0, 'snake':0, 'window360':0}
    outCount = 1
    posCount = 0
    
    prv_count = 0
    
    print("set-up complete")

    while True:
            try:
                sleep(0.1)

                #check movement type
                data1 = pd.read_csv('input1.txt', skiprows=[i for i in range(10)], nrows=50, header=None).values
                if len(data1) == 50 and not np.array_equal(old_data1, data1):
                    old_data1 = data1
                    moveType_1 = dance_or_position(data1)
                    print("dancer 1 is " + moveType_1)
                    
                data2 = pd.read_csv('input2.txt', skiprows=[i for i in range(10)], nrows=50, header=None).values
                if len(data2) == 50 and not np.array_equal(old_data2, data2):
                    old_data2 = data2
                    moveType_2 = dance_or_position(data2)
                    print("dancer 2 is " + moveType_2)
                    
                data3 = pd.read_csv('input3.txt', skiprows=[i for i in range(10)], nrows=50, header=None).values
                if len(data3) == 50 and not np.array_equal(old_data3, data3):
                    old_data3 = data3
                    moveType_3 = dance_or_position(data3)
                    print("dancer 3 is " + moveType_3)
                
                #update global position
                line_count = 0
                file = open('positions.txt', "r")
                Lines = file.readlines()
                for line in Lines:
                    line_count += 1
                    serPosition = line.strip()
                if (line_count > prv_count):
                    prv_count = line_count
                    update_position(serPosition)
                    output_p = serPosition
                    print("updated global position to " + serPosition)
                
                #positioning
                if (moveType_1 == 'positioning' or moveType_2 == 'positioning' or moveType_3 == 'positioning'):
                    posCount = 0
                    if (moveType_1 == 'positioning'):
                        posCount += 1
                    if (moveType_2 == 'positioning'):
                        posCount += 1
                    if (moveType_3 == 'positioning'):
                        posCount += 1
                    if (posCount > 1 and isMove == False):
                        #check stop moving
                        if (not done1):
                            motion1 = pd.read_csv('input1.txt', skiprows=[i for i in range(10)], header=None).values
                            len1 = len(motion1)
                            if len1 > old1:
                                old1 = len1
                            elif len1 == old1:
                                done1 = True
                        if (not done2):
                            motion2 = pd.read_csv('input2.txt', skiprows=[i for i in range(10)], header=None).values
                            len2 = len(motion2)
                            if len2 > old2:
                                old2 = len2
                            elif len2 == old2:
                                done2 = True
                        if (not done3):
                            motion3 = pd.read_csv('input3.txt', skiprows=[i for i in range(10)], header=None).values
                            len3 = len(motion3)
                            if len3 > old3:
                                old3 = len3
                            elif len3 == old3:
                                done3 = True
                            
                        if (done1 and done2 and done3):
                            done1 = False
                            done2 = False
                            done3 = False
                            old1 = -1
                            old2 = -1
                            old3 = -1
                            output_p = positioning()
                            isMove = True
                            print("new position is " + output_p)

                #dancer1
                if (moveType_1 == 'dancing'):
                    data_1 = pd.read_csv('input1.txt',skiprows=[i for i in range(40)], header=None).values
                    len_1 = len(data_1)
                    if len_1 > 80:
                        new_data_1 = pd.read_csv('input1.txt', skiprows=[i for i in range(40)], nrows=80, header=None).values
                        if(not np.array_equal(old_data_1, new_data_1)):
                            isPredicted_1 = True
                            old_data_1 = new_data_1
                            test_1 = data_preprocessing(new_data_1)
                            count[run_predict(test_1)] += 1
                            print("predicted 1")

                #dancer2
                if (moveType_2 == 'dancing'):
                    data_2 = pd.read_csv('input2.txt',skiprows=[i for i in range(40)], header=None).values
                    len_2 = len(data_2)
                    if len_2 > 80:
                        new_data_2 = pd.read_csv('input2.txt', skiprows=[i for i in range(40)], nrows=80, header=None).values
                        if(not np.array_equal(old_data_2, new_data_2)):
                            isPredicted_2 = True
                            old_data_2 = new_data_2
                            test_2 = data_preprocessing(new_data_2)
                            count[run_predict(test_2)] += 1
                            print("predicted 2")

                #dancer3
                if (moveType_3 == 'dancing'):
                    data_3 = pd.read_csv('input3.txt',skiprows=[i for i in range(40)], header=None).values
                    len_3 = len(data_3)
                    if len_3 > 80:
                        new_data_3 = pd.read_csv('input3.txt', skiprows=[i for i in range(40)], nrows=80, header=None).values
                        if(not np.array_equal(old_data_3, new_data_3)):
                            isPredicted_3 = True
                            old_data_3 = new_data_3
                            test_3 = data_preprocessing(new_data_3)
                            count[run_predict(test_3)] += 1
                            print("predicted 3")
                    
                #write to file if dance predictions done
                if (isPredicted_1 == True and isPredicted_2 == True and isPredicted_3 == True):
                    isPredicted_1 = False
                    isPredicted_2 = False
                    isPredicted_3 = False
                    isMove = False
                    moveType_1 = 'nil'
                    moveType_2 = 'nil'
                    moveType_3 = 'nil'
                    file = open("output.txt","a+")
                    file.seek(0)
                    data = file.read(5)
                    if len(data) > 0:
                        file.write("\n")
                    predicted = output_p + "|" + max(count, key=count.get)
                    file.write(predicted)
                    file.close()
                    count = {'cowboy':0, 'mermaid':0, 'dab':0, 'jamesbond':0, 'logout':0, 'pushback':0, 'scarecrow':0, 'snake':0, 'window360':0}
                    print("--- output " + str(outCount) + " done: " + predicted + " ---")
                    outCount += 1
                    
            except pandas.io.common.EmptyDataError:
                continue
            
            except Exception as e:
                continue
            
if __name__ == "__main__":
    main()

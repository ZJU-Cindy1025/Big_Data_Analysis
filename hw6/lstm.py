import time

import pandas as pd
from keras.datasets.boston_housing import load_data

#x_train,y_train,x_test,y_test,window=load_data('C://Users//yyhzj//Desktop//lstm//data.csv',50,True)
x_train = pd.read_csv('hw6/train.csv', header=None)
x_test = pd.read_csv('hw6/test.csv', header=None)
val_x = pd.read_csv('hw6/val.csv', header=None)
x_train = x_train.values
val_x = val_x.values
x_test = x_test.values
x_train, y_train = x_train[:-24, :], x_train[24:, ]
x_test, y_test = x_test[:-24, :], x_test[24:, ]
x_validation, y_validation = val_x[:-24, :], val_x[24:, ]

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_validation = x_validation.reshape(x_validation.shape[0],x_validation.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

#构建LSTM神经网络模型进行预测
from keras.models import Sequential
from keras.layers import Bidirectional,LSTM
from keras.layers import Dense, Activation,Dropout

model = Sequential() #layer[1,50,50,50,50,1]
model.add(LSTM(input_shape=(None,1), units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(input_shape=(None,50), units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(input_shape=(None,50), units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))
model.add(Activation("linear"))
#model.add(Activation("sigmoid"))
start=time.time()
model.compile(loss='mse', optimizer='rmsprop')
print("compilation Time:",time.time()-start)

print(len(model.layers))
model.fit(x_train,y_train,batch_size=10,epochs=1,validation_data=(x_validation, y_validation), verbose=2)
score2=model.evaluate(x_test,y_test)
print(score2)


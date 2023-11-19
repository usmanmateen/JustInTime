import random
import math

def Sigmoid(x):
    return 1 / (1 + math.exp(-x))


def Parameters():
    num_inputs = int(input("Enter Input: "))
    hidden_units = int(input("Enter hidden_units: "))
    output_units = int(input("Enter output_units: "))
    learning_rate = int(input("Enter learning_rate: "))
    epochs = int(input("Enter epochs: "))

    activation_function = int(input("Enter Input: "))

    return num_inputs, hidden_units, output_units, learning_rate, epochs, activation_function
    


def Input(num_inputs):
    option = input(f'Enter (1) to enter inputs manually \n Enter (2) to load data from file \n Enter Value: ')
    inputs = []
    target = []
    if option == 1 or option == '1':
        for i in range(int(input("Enter total amount data entries: "))):
            print(f"Data input {i} ")
            data = [] 
            for each in range(num_inputs):
                value = int(input("Enter Value: "))
                data.append(value)

            data.append(int(input("Enter Target: ")))
            inputs.append(data)
    else:
        pass  #File read
    

    return inputs, target



def Structure(num_inputs, hidden_units, output_units): # 
    hidden_weights = []
    hidden_layer_one = []
    hidden_layer_two = []
    
    for each in num_inputs:  # for number of inputs 
        weight = [] 
        for i in hidden_units:
            weight.append(random.random()) # 2d Array for each weights link each array within is weight of each node connect.
        
        hidden_weights.append(weight)

    for each in hidden_units:
        weight = []
        for i in output_units:
            weight.append(random.random())
        
        hidden_layer_one.append(weight)
    
    for each in hidden_layer_one:
        hidden_layer_two.append(random.random())

    return hidden_weights, hidden_layer_one, hidden_layer_two
    


def Initalise(hidden_weights, hidden_layer_one, hidden_layer_two):
        return hidden_weights, hidden_layer_one, hidden_layer_two





def Output(hidden_weights, hidden_layer_one, hidden_layer_two, inputs, activation_function):
    hidden_layer_one_units = []
    hidden_layer_two_units = []


    for i in range(len(hidden_weights)):
        total = 0 
        for j in range(len(hidden_weights[i])):
            total += inputs[j] * hidden_weights[i][j]
        
        hidden_layer_one_units.append( Sigmoid(total) )
        
    
    for i in range(len(hidden_layer_one)):
        total = 0 
        for j in range(len(hidden_layer_one[i])):
            total += hidden_layer_one_units[j] * hidden_weights[i][j]
        
        hidden_layer_two_units.append( Sigmoid(total) )
    
    output = 0
    for i in range(len(hidden_layer_two)):  #2nd layer should be 1d array as there is only one output 
        output += hidden_layer_two[i] * hidden_layer_two_units[i]

    return Sigmoid(output)
         
        
def WeightUpdate(hidden_weights,hidden_layer_one,hidden_layer_two):
    pass


def Introduced(inputs,num_inputs,activation_function,epochs,hidden_weights, hidden_layer_one, hidden_layer_two):

    for i in range(epochs):
        random.shuffle(inputs) #randomises inputs values 


                


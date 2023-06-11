from tensorflow import keras
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

def create_rnn(input_neurons, num_hidden_layers, hidden_neurons, output_neurons):
    """
    Create an RNN model with the specified architecture.
    
    Args:
    input_neurons (int): The number of input neurons.
    num_hidden_layers (int): The number of hidden layers.
    hidden_neurons (int): The number of neurons in each hidden layer.
    output_neurons (int): The number of output neurons.
    
    Returns:
    Keras model: The RNN model with the specified architecture.
    """
    model = keras.models.Sequential()
    if num_hidden_layers == 1:
        model.add(keras.layers.SimpleRNN(
            units=hidden_neurons, input_shape=(None, input_neurons)))
    else:
        model.add(keras.layers.SimpleRNN(units=hidden_neurons,
                  return_sequences=True, input_shape=(None, input_neurons)))
        for _ in range(num_hidden_layers):
            model.add(keras.layers.SimpleRNN(
                units=hidden_neurons, return_sequences=True))
        model.add(keras.layers.SimpleRNN(units=hidden_neurons))
    model.add(keras.layers.Dense(units=output_neurons))
    return model


def save_model_structure(model, filename):
    """
    Save the structure of a Keras model as a Python code to a file.
    
    Args:
    model (Keras model): The model whose structure to save.
    filename (str): The name of the file to save the model structure to.
    """
    with open(filename, 'w') as file:
        file.write("from tensorflow import keras\n")
        file.write("def create_model():\n")
        file.write("    model = keras.models.Sequential()\n")
        for layer in model.layers:
            layer_config = layer.get_config()
            layer_type = type(layer).__name__
            layer_name = layer.name
            file.write(
                f"    {layer_name} = keras.layers.{layer_type}(**{layer_config})\n")
            file.write(f"    model.add({layer_name})\n")
        file.write("    return model\n")


def create_and_save_rnn(input_neurons, num_hidden_layers,
                        hidden_neurons, output_neurons):
    """
    Create an RNN and save its structure as a Python code to a file.
    """

    model = create_rnn(input_neurons, num_hidden_layers,
                       hidden_neurons, output_neurons)

    save_model_structure(model, "E:\fyp1\WebAppFlask\rnn_structure.py")

    print("RNN structure saved to rnn_structure.py")


def create_ann(num_input_neurons, num_hidden_layers, num_neurons_per_hidden_layer, num_output_neurons):
    model = Sequential()
    # Input layer
    model.add(Dense(num_neurons_per_hidden_layer,
              input_dim=num_input_neurons, activation='relu'))
    # Hidden layers
    for i in range(num_hidden_layers):
        model.add(Dense(num_neurons_per_hidden_layer, activation='relu'))
    # Output layer
    model.add(Dense(num_output_neurons, activation='softmax'))
    return model


def save_ann_structure(model, file_name):
    with open(file_name, 'w') as f:
        f.write("from keras.models import Sequential\n")
        f.write("from keras.layers import Dense\n\n")
        f.write("def create_ann():\n")
        f.write("\tmodel = Sequential()\n")
        for layer in model.layers:
            config = layer.get_config()
            name = layer.__class__.__name__
            f.write(f"\tmodel.add({name}(**{config}))\n")
        f.write("\treturn model\n")





def create_and_save_ann(input_neurons, num_hidden_layers,hidden_neurons, output_neurons):

    # Create and save the ANN
    ann_model = create_ann(input_neurons, num_hidden_layers,
                           hidden_neurons, output_neurons)
    save_ann_structure(ann_model , "ann_model.py")


def create_cnn(num_conv_layers, num_dense_layers, dense_layer_size, num_output_neurons):
    input_shape = (28, 28, 1)
    filters_per_layer = [32] * num_conv_layers
    kernel_size = (3, 3)
    pool_size = (2, 2)
    model = Sequential()
    # Convolutional layers
    for i in range(num_conv_layers):
        if i == 0:
            model.add(Conv2D(
                filters_per_layer[i], kernel_size=kernel_size, activation='relu', input_shape=input_shape))
        else:
            model.add(
                Conv2D(filters_per_layer[i], kernel_size=kernel_size, activation='relu'))
        model.add(MaxPooling2D(pool_size=pool_size))
    # Flatten layer
    model.add(Flatten())
    # Dense layers
    for i in range(num_dense_layers):
        model.add(Dense(dense_layer_size, activation='relu'))
    # Output layer
    model.add(Dense(num_output_neurons, activation='softmax'))
    return model


def save_cnn_structure(model, file_name):
    with open(file_name, 'w') as f:
        f.write("from keras.models import Sequential\n")
        f.write("from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense\n\n")
        f.write("def create_cnn():\n")
        f.write("\tmodel = Sequential()\n")
        for layer in model.layers:
            config = layer.get_config()
            name = layer.__class__.__name__
            f.write(f"\tmodel.add({name}(**{config}))\n")
        f.write("\treturn model\n")


def create_and_save_cnn(num_conv_layers, num_dense_layers,
                        dense_layer_size, num_output_neurons):


        # Create and save the CNN
    cnn_model = create_cnn(num_conv_layers, num_dense_layers,
                        dense_layer_size, num_output_neurons)
    save_cnn_structure(cnn_model, "cnn_model.py")

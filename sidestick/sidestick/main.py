import inp2com

# create a nex thread
listen_button = inp2com.Button_Pushed()
listen_button.start()

# start ivy and bindings
inp2com.init_ivy()

# wait the end
listen_button.join()

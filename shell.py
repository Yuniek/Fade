import fade

env = fade.Environment()
while True:
    text = input('fade > ')

    if text == 'bye()': exit()

    try:
        result = fade.run(text, env, 2)
        if result is not None:
            print(result)
            
    except fade.FadeError as error:
        print(error)
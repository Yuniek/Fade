import fade

env = fade.environment
while True:
    text = input('fade > ')

    if text == 'bye()': exit()


    try:
        result = fade.run(text, env)
        if result is not None:
            print(result)
            
    except fade.FadeError as error:
        print(error)
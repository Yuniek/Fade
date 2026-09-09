import fade

env = fade.Environment()
while True:
    text = input('fade > ')

    if text == 'bye()': exit()

    try:
        results = fade.run(text, env)
        for result in results:
            if result is not None:
                print(result)
            
    except fade.FadeError as error:
        print(error)
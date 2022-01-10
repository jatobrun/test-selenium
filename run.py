from src.main import Espol

print('Test-Selenium: Andres Torres')
res = input('Empezar (y/n): ')
print('Se esta ejecutando el primer ejercicio')
if res.lower() == 'y':
    with Espol(teardown=True) as bot:
        bot.landing_page_action()
        majors = bot.exercise_1()
        res = input('Deseas conocer las universidades con ABET? (y/n): ')
        if res.lower() == 'y':
            bot.exercise_2(majors)
        else:
            exit()
else: 
    exit() 

    

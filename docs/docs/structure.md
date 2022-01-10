---
sidebar_position: 2
---

# Structure

## Files

This project have 2 folders `src and docs`, in src folder is all the code of the test.

In src folder are 1 folder (static folder) and 5 python files (__init_.py, elements.py, locators.py, main.py and page.py)

- init.py -> I create this file for create a module
- elements.py -> In this file was all the code about the elements, getters, setter, base element, and the other elements like the **[documentation](https://selenium-python.readthedocs.io/page-objects.html)**.
- locators.py -> in this file I use XPATH for locating all the elements in the html page and a use the same metodology than the elements.py, for more info, follow the **[documentation](https://selenium-python.readthedocs.io/page-objects.html)**.
- main.py -> Is more the class file for the bot, in this file maybe in the future can i implement unittest library.
- page.py -> Is more the selenium code, and this file contents all the pages that i used to complete the test.
- run.py -> Is more the CLI for the project and this exceute all the other files.

## Thoughts

1. I learn selenium for about 1 day, then i began to start the project.
2. I try to use less cantity of for loops this was the real challenge because i can not have a large Big O (for example exponencial o cuadratic) I want to stay in a linear way maybe.
3. For the second part I use the first one and create a dicctionary, I love dicctionary with arrays, is a easy way to locate and element with many attributes and with this dicctionary i create the csv too (so 2 taks in a arrow)
4. I want to implement CI pipelines integration with github actions and unittest library integration but for the covid and was a weekend i cant.
5. I use POO for most of the code.
6. I can use lint tools to increase the redability of my code (Pep8).
7. I can use log tools to debug my code.


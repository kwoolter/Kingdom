# Kingdom
:copyright: 2019 kwoolter :monkey:

## About

Python version of the old BBC Micro game Yellow River Kingdom.

Still work in progress as no graphics yet!

## Intro
* Run `run.py` and start the CLI
* Type `start` to get going
* Type `play` to start your next turn

## BBC Version

You can play the original "Yellow River Kingdom" here:-

(http://bbcmicro.co.uk//index.php)

To get the game rules and calculations I looked at the BBC Basic source code by quitting the game and using the `LIST` 
command to pick my through it.

Here is an example procedure that shows the logic used to calculate how much rice was grown each season (`G`) 
and how many people died from starvation (`ST`):

<img src="https://github.com/kwoolter/Kingdom/blob/master/BBC%20Basic/SourceCode1.PNG" alt="code1">

Here is the code to calculate how many people the thieves killed (`TD`) and how much rice they stole (`TF`):

<img src="https://github.com/kwoolter/Kingdom/blob/master/BBC%20Basic/SourceCode2.PNG" alt="code2">




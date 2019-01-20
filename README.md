# Kingdom
:copyright: 2019 kwoolter :monkey:

## About
Python version of the old BBC Micro game 'Yellow River Kingdom' (aka 'Kingdom') that came on the `Welcome` cassette and was written by these legends in 1981:-
* Tom Hartley
* Jerry Temple-Fry
* Richard G Warner

### Intro
* Written in python 3
* Run `python run.py` to start the command line interface
* Type `start` to get going
* Type `play` to start your next turn
* Keep typing `play` to start your next turn

<img height="400" width="313" src="https://github.com/kwoolter/Kingdom/blob/colorama_version/view/screenshots/pyKingdom.png?raw=true" alt="game2">

## Python Version

This Python re-write is radically different in structure to the original!  It is a total re-write! More to follow on this.
Uses `colorama` package to make the text output more exciting.

## BBC Micro Version

You can play the original "Yellow River Kingdom" here:-

(http://bbcmicro.co.uk//index.php)

To get the game rules and calculations I looked at the BBC Basic source code by quitting the game and using the `LIST` 
command to pick my way through it.

Subsequently I found the source code here:-

(http://brandy.matrixnetwork.co.uk/examples/KINGDOM)

<img height="250" width="400" src="https://raw.githubusercontent.com/kwoolter/Kingdom/master/BBC%20Basic/bbc_screenshot.PNG" alt="game1">

### Code
The orignal code is very compact, has virtually no comments, uses short variable names and a lot of `GOTO` flow control.

Here is an example procedure that shows the logic used to calculate how much rice was planted and harvested each season (`G`) 
and how many people died from starvation (`ST`):

```
 6000 DEF PROCCALCULATE
 6010 IF B=0 THEN G=0:GOTO6100
 6020 ON S GOTO 6100,6030,6050
 6030 IF G>1000 THEN G=1000
 6040 G=G*(B-10)/B:GOTO6100
 6050 IF G<0 THEN 6100
 6060 G=18*(11+RND(3))*(0.05-1/B)*G
 6070 IF G<0 THEN 6100
 6080 F=F+INT(G)
 6100 ST=0:P=A+B+C:IF P=0 THEN 6299
 6110 T=F/P:IF T>5 THEN T=4:GOTO6200
 6120 IF T<2 THEN P=0:GOTO6299
 6130 IF T>4 THEN T=3.5:GOTO6200
 6140 ST=INT(P*(7-T)/7):T=3
 6200 P=P-ST:F=INT(F-P*T-ST*T/2)
 6210 IF F<0 THEN F=0
 6299 ENDPROC
```

Here is the code to calculate how many people the thieves killed (`TD`) and how much rice they stole (`TF`):
```
 5400 ON S GOTO 5410,5420,5430
 5410 I=200+RND(70)-C:GOTO5440
 5420 I=30+RND(200)-C:GOTO5440
 5430 I=RND(400)-C
 5440 I=INT(I):IF I<0 THEN I=0
 5450 TD=INT(C*I/400):C=C-TD
 5460 TF=INT(I*F/729+RND(2000-C)/10):IF TF<0 THEN TF=0
 5470 IF TF>2000 THEN TF=1900+RND(200)
 5480 F=F-TF
 5499 ENDPROC
```

Here is the code to calculate how many people were killed in the flood (`FD`), how much stored rice was lost (`FF`) 
and how much planted rice was lost (`G`).
```
 5790 VF=FL(1)+FL(2)+FL(3)
 5800 OP=A+B+C
 5810 A=INT((A/10)*(10-FS))
 5820 B=INT((B/10)*(10-FS))
 5830 C=INT((C/6)*(6-VF))
 5840 FF=INT(F*VF/6):F=F-FF
 5850 FD=OP-A-B-C
 5860 IF S=2 THEN G=G*(20-FS)/20
 5870 IF S=3 THEN G=G*(10-FS)/10
 5899 ENDPROC
```


If you want to delve deeper into the BBC Basic Code here are some helpers.

### Variables

Variable | Purpose
--- | ------------------
`P` | Population
`F` | Stored Food Supplies
`S` | Current Season
`Y` | Current Year
`A`| People to defend the dyke
`B`| People to work in the fields
`C`| People to defend the villages
`G`|Baskets of rice to be planted in the fields
`FD`|Flood deaths
`TD`|Thief attack deaths
`ST`|Starvation deaths
`FF`|Stored food lost if floods
`TF`|Stored food taken by thieves
`VF`|Villages caught in the floods

### Procedures

Procedure | Line | Purpose
---|----|----------------------
`DEF PROCNEWSEASON`|3000|Start a new season
`DEF PROCATTACK`|5000|Thief attack logic
`DEF PROCFLOOD`|5500|Flood logic
`DEF PROCCALCULATE`|6000|Season end logic


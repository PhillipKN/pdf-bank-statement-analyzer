 ![alt text](https://cdn-images-1.medium.com/max/2560/1*oCOdiQV4gjaYpkp912gEIQ.gif)
 
 ## Introduction 👋

<br />
 Like me, do you always wonder where your money goes each month
 and would like to get some insights into your spending? Here's how.
 Using Python, you can go from a PDF bank statement to a spend
 insight dashboard built with Python.
<br />
<br />

 Before trying tabula-py, check your environment via tabula-py environment_info() function,
 which shows Python version, Java version, and your OS environment.

 check java version: 
 
 !java -version

 Run this command to install tabula:

 !pip install -q tabula-py


## Code
There are three (3) Python scripts.
- <b>parameters</b>: contains the bulk of the code, i.e. parsing data from a PDF bank statement, data cleaning, and manual classification of transactions.

- <b>plots</b>: contains all the functions for creating the various plots.

- <b>panel_spend_dashboard</b>: contains the [Panel](https://panel.holoviz.org/) code for putting the final dashboard view together.

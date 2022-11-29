## ✨ Demo
 ![alt text](https://cdn-images-1.medium.com/max/2560/1*oCOdiQV4gjaYpkp912gEIQ.gif)
 
 ## Introduction 👋
 This repo contains code used for writing the article [Visualize your PDF Bank Statement with Python](https://python.plainenglish.io/visualize-your-pdf-bank-statement-with-python-cc3608d72a3) on Medium.
 
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


## 🚀 Usage
There are three (3) Python scripts.
- <b>parameters</b>: contains the bulk of the code, i.e. parsing data from a PDF bank statement, data cleaning, and manual classification of transactions.

- <b>plots</b>: contains all the functions for creating the various plots.

- <b>panel_spend_dashboard</b>: contains the [Panel](https://panel.holoviz.org/) code for putting the final dashboard view together.

## 📝 License

Copyright © 2019 [Phillip Heita](https://github.com/PhillipKN).<br />
This project is [MIT](https://github.com/PhillipKN/pdf-bank-statement-analyzer/blob/main/LICENSE) licensed.


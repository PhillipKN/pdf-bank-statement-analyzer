import param
import panel as pn
import io
import plotly.express as px
from plots import *
from parameters import p_s, p_e, bal_s, bal_e, vol_val_table

pn.extension('plotly')

# Dashboard Title, Logo, and Subtitle
# set a logo,title, and subtitle for your dashboard
logo  = """<a href="http://panel.pyviz.org">
           <img src="https://cdn.searchenginejournal.com/wp-content/uploads/2019/07/shutterstock_1153076705.png"
            width=200px height=100px align="center" margin=20px>"""

title = '# Spend Dashboard - Version 2.1'
t1 = pn.pane.HTML('<marquee width=200><b>Estimated Salary date and Net Income:</b></marquee>')
#t2 = pn.pane.HTML('<marquee width=200><b>Second approach:</b></marquee>')
subtitle = "Bank statement analysis is the analysis of the financial transactions of borrowers i.e. outflows or debits and inflows or credits over a period of time, based on their bank statements. Everyone has a bank statement, a universal document that contains all of their transaction histories. A bank statement is unequivocally the most valid record of one’s income and expenses and gives a fair view of one’s financial health."

# Put the dashboard together
tab_dashboard = pn.Row(
        pn.Column(
                  "#### Statement Period: {0}-{1}".format(p_s, p_e),
                  "#### Opening Balance: {0}".format(bal_s),
                  "#### Closing Balance: {0}".format(bal_e)#, t1, df_sal_1
                  ),
        pn.Column(amount_trend, balance_trend),
        pn.Column(trns_preference, merch_preference),
        pn.Column(vol_val_table, #"#### The balance after 7 days",
                  #"#### Average number of days taken to deplete funds",
                  #f"#### Average number of unpaids: {avg_no_unpaids}",
                  #"#### Total Number of Insufficient fund notifications"
                  ),  # draw chart function!
        sizing_mode='stretch_both')

# create the Panel object, passing in all smaller objects
'''First we create our single row. Then, we fill it with the contents of two columns.
Our first column will contain our 1) title, 2) subtitle, 3) dropdown and 4) date slider.
The second column will display the chart.'''
dashboard = pn.Column(logo, title, subtitle,tab_dashboard)
dashboard.show()

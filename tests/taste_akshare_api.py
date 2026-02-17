import akshare as ak

stock_notice_report_df = ak.stock_notice_report(symbol='持股变动', date="202602")
print(stock_notice_report_df[stock_notice_report_df['代码']=="301571"]['网址'][0])
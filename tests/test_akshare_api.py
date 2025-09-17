import akshare as ak

stock_notice_report_df = ak.stock_notice_report(symbol='财务报告', date="20240613")
print(stock_notice_report_df)
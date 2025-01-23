import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    print("SMTPサーバーへの接続に成功しました")
    server.quit()
except Exception as e:
    print(f"SMTPサーバーへの接続に失敗しました: {e}")

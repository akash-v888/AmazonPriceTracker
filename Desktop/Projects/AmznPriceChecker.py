import bs4
import urllib.request
import smtplib
import time

prices_list = []

def check_price():
    #paste item url
    url = ''

    sauce = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")

    prices = soup.find(id="priceblock_ourprice").get_text()
    prices = float(prices.replace(",", "").replace("$", ""))
    prices_list.append(prices)
    return prices

# sends a self-email to the supplied email. Requires password :(
def notify(message, email, pword):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email, pword)
    s.sendmail(email, message)
    s.quit()

# checks if the prices has decreased compared to the previous price in list
def didPriceDecrease(price_list):
    return prices_list[-1] < prices_list[-2]

# continouously checks item's price
count = 1
while True:
    current_price = check_price()
    if count > 1:
        flag = didPriceDecrease(prices_list)
        if flag:
            decrease = prices_list[-1] - prices_list[-2]
            message = f"The price decrease by {decrease} dollars since it's last update."
            notify(message)
    time.sleep(43000)
    count += 1
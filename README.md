# shamebot
## update your teams!

yahoo fantasy baseball has a league info page that shows you "last league activity" per manager.
shamebot is an automated service that scrapes that page, and emails the league if any manager has left their team adrift.

shamebot uses [@jbrudvik](https://github.com/jbrudvik)'s [yahooscraper](https://github.com/jbrudvik/yahooscraper) (because unfortunately the yahoo API doesn't provide manager activity) and [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/) to get the data, and the python bindings for [mandrill](http://mandrillapp.com/) to send email. :+1::+1: to all of those for existing.
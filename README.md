# shamebot

### overview
yahoo fantasy baseball has a league info page that shows you "last league activity" per manager.
shamebot is an automated service that scrapes that page, and emails the league if any manager has left their team adrift.

shamebot uses [@jbrudvik](https://github.com/jbrudvik)'s [yahooscraper](https://github.com/jbrudvik/yahooscraper) (because unfortunately the yahoo API doesn't provide manager activity) and [beautifulsoup](http://www.crummy.com/software/BeautifulSoup/) to get the data, and the python bindings for [mandrill](http://mandrillapp.com/) to send email. :+1::+1: to all of those for existing.

### deploying
shamebot is designed to be deployed on heroku, although I suppose if you could just set it as a cron task, if you have access to a server.

**deploying on heroku**

nb - all of the steps below are free.

1. fork this project into a personal repo.  clone it onto your local machine.
2. get a heroku account.  create a new app.  in git or on the command line, follow the instructions to add a heroku remote.
3. sign up for mandrill.  get an API key.
4. create a template in outbound > templates called `shame`.  here's the full text of mine:
```
Dear HPK,<br><br>*|ownerName|* has no league activity in the past *|dayValue|* days!<br><br>Always vigilant,<br>-shamebot<br><br><div style="font-size:10px">sent at *|DATE:D, d M Y H:i:s|*</div>
```
5. add all of the variable referenced in [main.py/os.environ](https://github.com/almartin82/shamebot/blob/3bcdd7c6dafd3f1ef7943406dba493bd66677ddf/main.py#L87) (roughly line 90) as config variables on heroku.
6. edit the receipt email in [line 123](https://github.com/almartin82/shamebot/blob/3bcdd7c6dafd3f1ef7943406dba493bd66677ddf/main.py#L124) so that you, the shamebot owner, get a run receipt, not me.
7. link your heroku account to your github repo.  make sure the settings are such that new commits to master trigger a heroku build.
8. add the heroku scheduler add on to your heroku app.  tell the scheduler `run python main.py` once a day, at whatever time you would like.
9. commit your changes to git and push to master.  heroku will pick them up and deploy your app.  scheduler will run main.py once a day.  you're in business!

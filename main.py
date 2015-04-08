import requests
import yahooscraper as ys
import urlparse
import BeautifulSoup
import pandas
from datetime import datetime
from time import gmtime, strftime
import mandrill
import os

def bootleg_session(user, password):
    """
    to get around SSLError: hostname problems
    http://stackoverflow.com/questions/22758031/how-to-disable-hostname-checking-in-requests-python
    we need to set verify=False in the requests call.
    yeah, I should move to python 3.4 to make sure that we're checking
    the cert, or someone can MITM me, but it's just my stupid yahoo
    fantasy baseball data & login.  whatever.
    """

    session = requests.Session()
    session.headers.update(ys.login.headers())
    response = session.get(ys.login.url(), verify=False)

    login_path = ys.login.path(response.text)
    login_post_data = ys.login.post_data(response.text, user, password)
    login_url = urlparse.urljoin(response.url, login_path)

    session.post(login_url, data=login_post_data)
    return session


def process_managerlist(page):
    """
    processes the team/manager page and returns a pandas df with
    each team's last login date (and num of moves/trades)
    """
    soup = BeautifulSoup.BeautifulSoup(page.text)
    table = soup.find('div', attrs={'id': 'teams'})
    table = table.find('table')
    table_body = table.find('tbody')

    data = []
    rows = table_body.findAll('tr')
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        if cols[0] != 'Co-Manager':
            data.append([ele for ele in cols if ele])

    df = pandas.DataFrame.from_dict(data)
    df[6] = pandas.to_datetime(df[5])
    df[7] = (datetime.now() - df[6]).astype('timedelta64[h]')
    return df


def shamebot(api_key, listhost, offender, num_days):
    """
    given an owner, days elapsed, and mandrill setup info,
    uses the mandrill python bindings to send out an email
    calling out the owner.
    """

    mandrill_client = mandrill.Mandrill(api_key)
    mandrill_client.messages.send_template(
        'shame',
        [],
        {'to': [{'email': listhost, 'name': 'Andrew Martin'}],
         'global_merge_vars':
             [
                 {'vars':
                      [{'name': 'ownerName', 'content': offender},
                       {'name': 'dayValue', 'content': num_days}]
                 }
             ],
         'merge_vars':
             [
                 {'rcpt': listhost,
                  'vars':
                      [{'name': 'ownerName', 'content': offender},
                       {'name': 'dayValue', 'content': num_days}]
                 }
             ]
        }
    )

league_url = os.environ['league_url']
y_user = os.environ['y_user']
y_pass = os.environ['y_pass']
api_key = os.environ['api_key']
listhost = os.environ['listhost']
shame_hours = os.environ['shame_hours']

print shame_hours

#make a session
session = bootleg_session(y_user, y_pass)

#fetch and parse the league page
shame = session.get(league_url, verify=False)
data = process_managerlist(shame)
#print data

#for logs
print data[7]
print data[7] > shame_hours

#send shamebot emails to owners who fit criteria
for index, row in data.iterrows():
    if row[7] > shame_hours:
        print 'criteria match!'
        print row[1]
        shamebot(
            api_key=api_key,
            listhost=listhost,
            offender=row[0] + ' (' + row[1] + ')',
            num_days=round(row[7] / 24, 1)
        )


#send receipt email to ALM
mandrill_client = mandrill.Mandrill(api_key)
message = {
    'from_email': 'shamebot@hpkdiaspora.com',
    'from_name': 'hpk shamebot',
    'subject': 'shamebot ran successfully',
    'text': 'heroku process ran at ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()),
    'to': [
        {'email': 'almartin@gmail.com',
         'name': 'Andrew Martin',
         'type': 'to'}]
}
result = mandrill_client.messages.send(message=message)
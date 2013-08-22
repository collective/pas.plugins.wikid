""" It's dedicated to testing purposes """

from .client import WikidClient

# You should set up input parameters (host, username, etc.) for this test.
# So, before executing this example you have to:
#  1) Install one of the token clients
#  (http://wikidsystems.com/downloads/token-clients)
#  2) Run your clients and push "Create New Domain",
#  enter "Server Code" and PIN. Please, remember a PIN because
#  it's you 'regcode' (see the method -'registerUsername' for details).
#  Push "Get Passcode" and you will get 'passcode' (see the method - 'login' for details)
#  3) Fill in other parameters.
w = WikidClient(host='127.0.0.1', port=8388, pkey='localhost.p12',
                pass_phrase='secret', cacert='WiKID-ca.pem')
w.setUpConnection()
# You will not verify your user if it's not registered.
# That's why you can find below the method - 'registerUsername'
# for this purpose. You should notice that values of parameters
# in methods 'login' and registerUsername are almost the same.
if w.login('testuser', 'passcode', '127000000001'):
    print 'Cool Valid user'
else:
    print 'No lah! No Entry!'
    # fill in 'regcode' which you get from a token client.
    print w.registerUsername('testuser', 'regcode', '127000000001')

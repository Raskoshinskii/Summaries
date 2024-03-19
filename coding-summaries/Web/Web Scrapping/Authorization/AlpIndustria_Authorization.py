import requests
from bs4 import BeautifulSoup

"""
Steps for a successful Login
1. Intercept POST request when submitting log in button (use INSPECT in a browser);
2. Find URL that we have to request for logging In
3. Find out the requested parameters that are sent with POST request (FORM DATA)
4. Create the same parameters (using a dictionary)
5. Send POST request with found parameters to the target URL

Website: https://sport-marafon.ru/
Always use Session to be always logged In
"""
# Found URL
url_to_log_in = 'https://sport-marafon.ru/include/auth/ajax/auth.php'
form_data = {
    'USER_LOGIN': 'email_here',
    'USER_PASSWORD': 'password_here',
    'backurl': '/',
    'AUTH_FORM': 'Y',
    'TYPE': 'AUTH',
    'AJAX_AUTH': 'Y',
    'Login': 'Войти'
}

# Logging In in a Session (We have to stay in a Session)
with requests.Session() as session:
    session.post(url_to_log_in, data = form_data)
    response = session.get('https://sport-marafon.ru/personal/profile/') # As we are Logged In we can access profile data
    print(response.status_code)

    # My name extraction from my profile
    html = BeautifulSoup(response.text, 'lxml')
    my_name = html.find('input', id = 'personal_profile_NAME').get('value')
    print(my_name)
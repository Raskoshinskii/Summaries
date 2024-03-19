"""
Website: https://sevashoes.com/en

The website doens't show prices till a user is authorized.
However, the authorization is tricky (there is a protection)

Always pay attention at the form itslef. There migh be some scripts
that change the input data. Likewise, check XHR and Doc filters in NETWORK

It turned out that there is a JavaScript: doChallengeResponse() on a form
that changeset the input data. Here is the function:

	function doChallengeResponse() {
		str = document.login_form.username.value + ":"
				+ hex_md5(document.login_form.password.value) + ":"
				+ document.login_form.challenge.value;
		document.login_form.password.value = "";
		document.login_form.challenge.value = "";
		document.login_form.response.value = hex_md5(str);
		return false;
	}

After analyzing the JS function we can say that:
1. Input data is being transformed into a str that has the following structure:

    str = username:md_5_hash_password:challenge_value

2. challenge_value is refreshed and generated each time (it can be extracted from the FORM)
3. Fianl output must have the following structure:
    password: '',
    challenge: '',
    response: md_5_hash(str)

4. Parameters above must be sent to https://sevashoes.com/en/login
"""

import requests
import hashlib # for md_5 hash getting
from bs4 import BeautifulSoup

with requests.Session() as session:
    log_in_url = 'https://sevashoes.com/en/login'

    # Step 1 (Form Data Creation)
    username = 'email_here'
    pwd = 'password_here'
    pwd_md5 = hashlib.md5(bytes(pwd, encoding = 'utf8')).hexdigest()

    # Step 1.1 Challenge Value Getting
    response = session.get(log_in_url)
    html = BeautifulSoup(response.text, 'lxml')
    challenge_value = html.find('input', id = 'challenge').get('value')

    # Step 1.2 Final String Getting
    target_str = f'{username}:{pwd_md5}:{challenge_value}'
    res_srt = hashlib.md5(bytes(target_str, encoding='utf8')).hexdigest()

    form_data = {
        'username': username,
        'password': '',
        'challenge': '',
        'response': res_srt
    }

    # Step 2 Logging In
    response = session.post(log_in_url, data = form_data)

    html = BeautifulSoup(response.text, 'lxml')
    items = html.select('div.col-xs-6')

    for item in items:
        try:
            name = item.find_all('div')[1].text.split('·')[1]
            price = item.find_all('div')[2].text.split('+')[0].lstrip('Precio: ')
            print(name, price)
        except:
            pass
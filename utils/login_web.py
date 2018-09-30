import click
import requests
from bs4 import BeautifulSoup
from ....utils.logging import logger

url = "https://www.codechef.com"


def login_web(self):
    global codechef_session
    codechef_session = self.session
    username = click.prompt('username')
    password = click.prompt('password', hide_input=True)
    login(username, password)
    session_data = {
        'cookies': codechef_session.cookies
    }
    logger.debug('returning session data\n %s' % session_data)
    return session_data


def login(username, password):
    login_url = url+"/"
    login_page = codechef_session.get(login_url)
    form_feilds = BeautifulSoup(login_page.text, "html.parser").findAll("input")
    form_data = {"pass": password,
                 "name": username}

    for i in form_feilds:
        attrs = i.attrs
        if "name" in attrs:
            if "value" in attrs and attrs["value"]:
                form_data[attrs["name"]] = attrs["value"]
    try:
        logged_page = codechef_session.post(login_url, form_data)
    except BaseException:
        raise
    else:
        # logout all other sessions as codechef doesn't allow multiple sessions
        if("session/limit" in logged_page.url):
            click.confirm("Session limit exceeded\n" +
                          "Do you want to logout of other sessions",
                          default=True, abort=True)
            logger.info("logging you out of all other sessions\n" +
                        "this may take some time...")
        if "session/limit" in logged_page.url:
            logout_other_session()

        # codechef doesn't check cookies and trivially displays
        # the latest as current session
        # handle this using modifying logout_other_session by
        # logging out after checking session cookies
        # and matching with form data. trivially the following solution works

        logged_page = codechef_session.post(url, form_data)
        if len(
            BeautifulSoup(
                logged_page.text,
                "html.parser").findAll("input")) > 0 and is_logged_in():
            click.confirm(
                "You are/have tried to login to codechef while" +
                "the script was running\nDo you want to try login again?",
                default=True,
                abort=True)
            login(username, password)
        else:
            if(is_logged_in()):
                return
            else:
                raise Exception("credential_error")


def logout_other_session():
    global codechef_session
    sess_url = url+"/session/limit"
    try:
        session_page = codechef_session.get(sess_url)
    except BaseException:
        raise

    form_feilds = BeautifulSoup(
        session_page.text,
        "html.parser").findAll("input")
    form_data = {}
    logger.debug(form_feilds)
    for j in range(len(form_feilds)-5):
        i = form_feilds[j]
        attrs = i.attrs
        if "name" in attrs:
            if "value" in attrs and attrs["value"]:
                form_data[attrs["name"]] = attrs["value"]
    for j in [-1, -2, -3, -4]:
        i = form_feilds[j]
        attrs = i.attrs
        if "name" in attrs:
            if "value" in attrs and attrs["value"]:
                form_data[attrs["name"]] = attrs["value"]
    try:
        # no need to assign to a variable
        logger.debug(form_data)
        codechef_session.post(sess_url, data=form_data)
    except BaseException:
        raise


def is_logged_in():
    global codechef_session
    user_url = "https://www.codechef.com/api/user/me"
    try:
        page = codechef_session.get(user_url).json()
    except BaseException:
        return None
    if(not page["user"]["username"]):
        return False
    else:
        return True

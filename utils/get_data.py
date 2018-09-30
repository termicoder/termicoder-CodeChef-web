from datetime import datetime
from ....utils.logging import logger


def transpose_running_web(x):
    return {
        'code': x['code'],
        'endDate': datetime.fromtimestamp(float(x['end_date'])),
        'startDate': datetime.fromtimestamp(float(x['start_date'])),
        'name': x['name']
    }


def transpose_running_oauth(x):
    return {
        'code': x['code'],
        'endDate': datetime.strptime(x['endDate'], '%Y-%m-%d %H:%M:%S'),
        'startDate': datetime.strptime(x['endDate'], '%Y-%m-%d %H:%M:%S'),
        'name': x['name']
    }


def running_contests(self):
    path = 'runningUpcomingContests/data' if self.CODECHEF_WEB else 'contests'
    url = self._make_url(path)
    r = self._request_api(url)
    if(self.CODECHEF_WEB):
        return map(transpose_running_web, r['contests'])

    data = r['result']['data']['content']
    contest_list = map(transpose_running_oauth, data['contestList'])
    current_time = datetime.fromtimestamp(data['currentTime'])

    def check_current(contest):
        contest_time = contest['endDate']
        return contest_time >= current_time

    running = list(filter(check_current, contest_list))
    logger.debug("got running")

    return running

#!/usr/bin/env python3
import os
import json
import requests
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import timedelta, datetime
from pytz import timezone


@dataclass
class Report:
    failed: int
    broken: int
    skipped: int
    passed: int
    unknown: int
    total: int
    start: int
    stop: int
    duration: int


@dataclass
class MattermostConf:
    bot_token: str
    chat_id: str


APP_HOST = "type_app_host"
DBG_MTR_CONF = MattermostConf(bot_token='xkq3x4hwbfyzpqxcunduqwzh3e', chat_id='ncwt6oesk7dopnnf71ouyzgw3o')
WORK_MTR_CONF = MattermostConf(bot_token='xkq3x4hwbfyzpqxcunduqwzh3e', chat_id='upzgqbezz3r6bncotdud9jgsgc')


class MattermostBot:
    def __init__(self, token, ssl_verify):
        self.token = token
        self.url = APP_HOST
        self.ssl_verify = ssl_verify

    def get(self, request):
        return requests.get(
                self.url + request,
                headers=self._get_headers(),
                verify=self.ssl_verify
            ).json()

    def post(self, request, data):
        return requests.post(
            self.url + request,
            headers=self._get_headers(),
            data=json.dumps(data),
            verify=self.ssl_verify
        ).json()

    def _get_headers(self):
        return {"Authorization": "Bearer " + self.token}

    def create_post(self, user_id, channel_id, message,
                    files=None, pid="", props=None):
        return self.post(
            '/posts',
            {
                'channel_id': channel_id,
                'message': message,
                'file_ids': files or [],
                'root_id': pid,
                'props': props or {}
            })

    def channel_msg(self, channel_id, message, files=None, pid="", props=None):
        return self.create_post(None, channel_id,
                                "{}".format(message), files, pid,
                                props=props or {})


def parse_allure_json(allure_report_dir: str) -> Report:
    """
    Парсинг allure отчета
    """
    path_to_file = os.path.join(allure_report_dir, 'widgets', 'summary.json')
    with open(path_to_file, "r", encoding='utf-8') as f:
        data = json.load(f)
    stats = data['statistic']
    times = data['time']
    return Report(stats['failed'], stats['broken'], stats['skipped'], stats['passed'], stats['unknown'],
                  stats['total'], times['start'], times['stop'], times['duration'])


def format_message(report: Report, report_url: str, job_name: str) -> str:
    """Подготовка сообщения."""
    start_time = datetime.fromtimestamp(report.start / 1000, tz=timezone('Europe/Moscow')).strftime("%d.%m.%Y %H:%M:%S")
    duration = "{:0>8}".format(str(timedelta(seconds=int(report.duration / 1000))))
    stand_name = f" ({os.environ['ENV']})" if job_name == 'oog-autotests_debug' else ''
    message = f"""### :chart_with_upwards_trend: Краткий отчет о запуске {job_name}{stand_name}:
:clock10: {start_time}

:arrow_forward: Всего тестов: {report.total}

| :heavy_check_mark: Успешно           | :heavy_multiplication_x: Провалено         | :wavy_dash: Пропущено         | :hourglass_flowing_sand: Время выполнения  | :pencil: Отчет             |
| :--------------:  |:---------------:  | :---------------: | :---------------: | :---------------:  |
| {report.passed} | {report.failed + report.broken} | {report.skipped} | {duration} | [Полный отчет]({report_url}) |
"""
    return message


def main():
    argparser = ArgumentParser('Парсинг и отправка результатов выполнения в Telegram чат')
    argparser.add_argument('-r', '--allure-report', type=str, dest='allure_report')
    argparser.add_argument('-u', '--build-url', type=str, dest='build_url')
    argparser.add_argument('-j', '--job_name', type=str, dest='job_name')
    argparser.add_argument('-chat_dest', '--chat_dest', type=str, dest='chat_dest')
    arguments = argparser.parse_args()

    if arguments.chat_dest == "work":
        mtr_conf = WORK_MTR_CONF
    else:
        mtr_conf = DBG_MTR_CONF

    try:
        report = parse_allure_json(arguments.allure_report)
        message = format_message(report, arguments.build_url + 'allure', arguments.job_name)
    except:
        message = 'Отчет по автотестам {job_name} не был сформирован :(\nЛог консоли: {log_url}'.format(
            log_url=arguments.build_url + 'console', job_name=arguments.job_name)

    _mattermost_reporter = MattermostBot(token=mtr_conf.bot_token, ssl_verify=False)
    _mattermost_reporter.channel_msg(channel_id=mtr_conf.chat_id, message=message)


if __name__ == '__main__':
    main()

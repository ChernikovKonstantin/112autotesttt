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


def format_message(report: Report, report_url: str, job_name: str, stand_name: str) -> str:
    """
    Подготовка сообщения
    """
    sep = '\U00002063'
    start_time = datetime.fromtimestamp(report.start / 1000, tz=timezone('Europe/Moscow')).strftime("%d.%m.%Y %H:%M:%S")
    duration = "{:0>8}".format(str(timedelta(seconds=int(report.duration / 1000))))
    message = f"""
        \U0001F4C8 {sep} *Краткий отчет о запуске {job_name} (stand = {stand_name}):*\n
        {sep} \U0001F563 {sep}   *{start_time}*\n
        {sep} \U000025B6 {sep}   Всего тестов:   *{report.total}*\n
        {sep} \U00002705 {sep}   Успешно:   *{report.passed}*\n
        {sep} \U0000274C {sep}   Провалено:   *{report.failed + report.broken}*\n
        {sep} \U00003030 {sep}   Пропущено:   *{report.skipped}*\n
        {sep} \U000023F3 {sep}   *{duration}*\n
        \U0001F517 {sep}   [Полный отчет]({report_url})        
        """
    return message


def send_message_to_telegram_chat(bot_id, bot_token, chat_id, msg):
    """
    Отправка сообщения в чат
    """
    a = requests.post(f'https://api.telegram.org/bot{bot_id}:{bot_token}/sendMessage',
                  json=dict(chat_id=chat_id, text=msg, parse_mode='Markdown'),
                  proxies=dict(http="socks5h://172.17.21.92:9050", https="socks5h://172.17.21.92:9050"))
    print(a.text)

def main():
    argparser = ArgumentParser('Парсинг и отправка результатов выполнения в Telegram чат')
    argparser.add_argument('-b', '--botid', type=str, dest='bot_id')
    argparser.add_argument('-t', '--token', type=str, dest='bot_token')
    argparser.add_argument('-c', '--chatid', type=str, dest='chat_id')
    argparser.add_argument('-r', '--allure-report', type=str, dest='allure_report')
    argparser.add_argument('-u', '--build-url', type=str, dest='build_url')
    argparser.add_argument('-j', '--job_name', type=str, dest='job_name')
    argparser.add_argument('-s', '--stand_name', type=str, dest='stand_name')
    arguments = argparser.parse_args()

    try:
        report = parse_allure_json(arguments.allure_report)
        message = format_message(report, arguments.build_url + 'allure', arguments.job_name, arguments.stand_name)
    except:
        message = '\U0001F432 Отчет по автотестам {job_name} (stand = {stand_name}) не был сформирован ' \
                  ':(\nЛог консоли: {log_url}'.format(
            log_url=arguments.build_url + 'console', job_name=arguments.job_name, stand_name=arguments.stand_name)
    send_message_to_telegram_chat(arguments.bot_id, arguments.bot_token, arguments.chat_id, message)


if __name__ == '__main__':
    main()

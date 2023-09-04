import time
import allure
import curlify
from requests import Request

from api.base_api.logger import logger


def allure_attach(description, data):
    if isinstance(data, (list, tuple)):
        if all([isinstance(d, str) for d in data]):
            data = '\n'.join(data)
        else:
            converted_data = []
            for d in data:
                try:
                    converted_data.append(d.__dict__)
                except:
                    converted_data.append(d)
            data = converted_data

    if not isinstance(data, str):
        data = str(data)

    allure.attach(data, description, allure.attachment_type.TEXT)


def current_timestamp():
    return int(time.time())


def replace_binary_data_in_request_body(request: Request):
    # replace binary data for string  '(binary)'
    if 'boundary' in request.headers.get('Content-Type', ''):
        request.body = '(binary)'
    return request


def filter_request_headers(request: Request):
    # leave only useful headers
    #header_list = ['Authorization', 'Content-Type', 'Cookie']
    header_list = ['Authorization', 'Content-Type']
    request.headers = {k: v for k, v in request.headers.items() if
                       k in header_list}
    return request


def debug_log(response):
    if response.history:  # redirect detected!
        for res in response.history:
            logger.debug('*** REDIRECT has been detected, url: "%s"' % res.request.url)
    # leave only useful headers and remove binary data from request
    request = filter_request_headers(
        replace_binary_data_in_request_body(
            response.request))
    logger.debug('>>> REQUEST: ' + curlify.to_curl(request))
    logger.debug('<<< RESPONSE STATUS CODE: {code}'.format(code=response.status_code))
    # logger.debug('<<< RESPONSE HEADERS: %s' % response.headers)
    response_text = response.text if 'text/html' not in \
                                     response.headers.get('Content-Type', '') else 'html source, do not save_and_send.'
    logger.debug('<<< RESPONSE BODY: ' + response_text)
    logger.debug('-' * 120)


def write_log(response):
    if not str(response.status_code).startswith('2'):
        debug_log(response)
        logger.warning('We have got response code %s with message: "%s"' % (
            response.status_code, response.content.decode('utf-8')))
        allure_attach('Bad status code', 'Status code:%s\n\nError message:\n%s\n' % (response.status_code,
                                                                                     response.content))

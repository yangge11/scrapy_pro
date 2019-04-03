# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import random
import time
from collections import defaultdict

from scrapy import signals
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.android import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from sh import TimeoutException
from selenium.webdriver import FirefoxOptions


class ScrapyDemoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyDemoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def get_bai_jia_response(self, spider, request):
        response = None
        if request.url == spider.login_url:
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            driver = webdriver.Firefox(executable_path=spider.DRIVER_FIREFOX_HOME, firefox_options=opts)
            driver.set_page_load_timeout(5)
            try:
                driver.get(request.url)
            except TimeoutException:
                logging.warn('time out 5s')
                element = WebDriverWait(driver, 120, 0.5).until(
                    expected_conditions.presence_of_element_located((By.ID, "TANGRAM__PSP_4__footerULoginBtn")))
                put_login = driver.find_element_by_id('TANGRAM__PSP_4__footerULoginBtn')
                put_login.click()
                time.sleep(random.randint(1, 5))

                name = driver.find_element_by_id('TANGRAM__PSP_4__userName')
                name.send_keys(request.meta['account']['user_name'])
                time.sleep(random.randint(1, 5))

                password = driver.find_element_by_id('TANGRAM__PSP_4__password')
                password.send_keys(request.meta['account']['pwd'])
                time.sleep(random.randint(1, 5))
                enter = driver.find_element_by_id('TANGRAM__PSP_4__submit')
                enter.click()
                time.sleep(5)
                # element = WebDriverWait(driver, 60, 0.5).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "client_pages_home")))
            while True:
                time.sleep(random.randint(30, 50))
                body = driver.page_source
                if '粉丝总人数' in body.encode('utf8'):
                    logging.debug('login success===> %s' % request.meta['account']['user_name'])
                    break
                try:
                    driver.refresh()
                    time.sleep(5)
                except:
                    logging.warn('refresh failed in %s' % request.meta['account']['user_name'])

            cookies = driver.get_cookies()
            account_cookie = {}
            for cookie in cookies:
                if 'name' in cookie.keys() and 'value' in cookie.keys():
                    account_cookie[cookie['name']] = cookie['value']
            request.meta['cookie'] = account_cookie
            response = HtmlResponse(url=driver.current_url, body=body.encode('utf-8'))
            driver.quit()
        return response


class ScrapyDemoDownloaderProxyMiddleWare(object):
    proxy_list = ["http://128.1.41.120:18283", ]

    def process_request(self, request, spider):
        ip = random.choice(self.proxy_list)
        request.meta['proxy'] = ip


class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    """
    代理中间件，为每一次请求提供随机代理
    """

    def __init__(self, auth_encoding='latin-1', proxy_list_file=None):
        if not proxy_list_file:
            raise NotConfigured
        self.auth_encoding = auth_encoding
        self.proxies = defaultdict(list)
        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['proxy_scheme']
                url = proxy['proxy']
                self.proxies[scheme].append(self._get_proxy(url, scheme))

    @classmethod
    def from_crawler(cls, crawler):
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'latain-1')
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')
        return cls(auth_encoding, proxy_list_file)

    def _set_proxy(self, request, scheme):
        creds, proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
        if creds:
            request.headers['Proxy-Authorization'] = b'Basic ' + creds


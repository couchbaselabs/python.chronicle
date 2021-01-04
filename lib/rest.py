import requests
import logging


class Rest(object):
    def __init__(self):
        self.log = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

    def http_session_get(self, api, headers=None, session=None, timeout=120):
        try:
            response = session.get(api, headers=headers, timeout=timeout)
            status = response.status_code
            content = response.content
            if status in [200, 201, 202, 204]:
                return True, content, response
            else:
                self.log.error(response.reason)
                return False, content, response
        except requests.exceptions.HTTPError as errh:
            self.log.error("HTTP Error {0}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            self.log.error("Error Connecting {0}".format(errc))
        except requests.exceptions.Timeout as errt:
            self.log.error("Timeout Error: {0}".format(errt))
        except requests.exceptions.RequestException as err:
            self.log.error("Something else: {0}".format(err))

    def http_session_post(self, api, params='', headers=None, session=None, timeout=120):
        try:
            response = session.post(api, headers=headers, data=params, timeout=timeout)
            status = response.status_code
            content = response.content
            if status in [200, 201, 202, 204]:
                return True, content, response
            else:
                self.log.error(response.reason)
                return False, content, response
        except requests.exceptions.HTTPError as errh:
            self.log.error("HTTP Error {0}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            self.log.error("Error Connecting {0}".format(errc))
        except requests.exceptions.Timeout as errt:
            self.log.error("Timeout Error: {0}".format(errt))
        except requests.exceptions.RequestException as err:
            self.log.error("Something else: {0}".format(err))

    def http_session_put(self, api, params='', headers=None, session=None, timeout=120):
        try:
            response = session.post(api, headers=headers, data=params, timeout=timeout)
            status = response.status_code
            content = response.content
            if status in [200, 201, 202, 204]:
                return True, content, response
            else:
                self.log.error(response.reason)
                return False, content, response
        except requests.exceptions.HTTPError as errh:
            self.log.error("HTTP Error {0}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            self.log.error("Error Connecting {0}".format(errc))
        except requests.exceptions.Timeout as errt:
            self.log.error("Timeout Error: {0}".format(errt))
        except requests.exceptions.RequestException as err:
            self.log.error("Something else: {0}".format(err))

    def http_session_delete(self, api, headers=None, session=None, timeout=120):
        try:
            response = session.get(api, headers=headers, timeout=timeout)
            status = response.status_code
            content = response.content
            if status in [200, 201, 202, 204]:
                return True, content, response
            else:
                self.log.error(response.reason)
                return False, content, response
        except requests.exceptions.HTTPError as errh:
            self.log.error("HTTP Error {0}".format(errh))
        except requests.exceptions.ConnectionError as errc:
            self.log.error("Error Connecting {0}".format(errc))
        except requests.exceptions.Timeout as errt:
            self.log.error("Timeout Error: {0}".format(errt))
        except requests.exceptions.RequestException as err:
            self.log.error("Something else: {0}".format(err))

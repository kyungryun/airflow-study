# -*- coding: utf-8 -*-

from builtins import str

from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults


class CustomHttpSensor(BaseSensorOperator):
    """
    Executes a HTTP get statement and returns False on failure:
        404 not found or response_check function returned False

    :param http_conn_id: The connection to run the sensor against
    :type http_conn_id: str
    :param method: The HTTP request method to use
    :type method: str
    :param endpoint: The relative part of the full url
    :type endpoint: str
    :param request_params: The parameters to be added to the GET url
    :type request_params: a dictionary of string key/value pairs
    :param headers: The HTTP headers to be added to the GET request
    :type headers: a dictionary of string key/value pairs
    :param response_check: A check against the 'requests' response object.
        Returns True for 'pass' and False otherwise.
    :type response_check: A lambda or defined function.
    :param extra_options: Extra options for the 'requests' library, see the
        'requests' documentation (options to modify timeout, ssl, etc.)
    :type extra_options: A dictionary of options, where key is string and value
        depends on the option that's being modified.
    """

    template_fields = ('endpoint', 'request_params', 'headers', 'response_check')

    @apply_defaults
    def __init__(self,
                 endpoint,
                 http_conn_id='http_default',
                 method='GET',
                 request_params=None,
                 headers=None,
                 response_check=None,
                 extra_options=None, *args, **kwargs):
        super(CustomHttpSensor, self).__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.http_conn_id = http_conn_id
        self.request_params = request_params or {}
        self.headers = headers or {}
        self.extra_options = extra_options or {}
        self.response_check = response_check

        self.hook = HttpHook(
            method=method,
            http_conn_id=http_conn_id)

    def poke(self, context):
        self.log.info('Poking: %s', self.endpoint)
        try:
            response = self.hook.run(self.endpoint,
                                     data=self.request_params,
                                     headers=self.headers,
                                     extra_options=self.extra_options)
            if self.response_check:
                # run content check on response
                # xcom_push 를 위해 context 정보도 리턴해줌
                return self.response_check(response, **context)
        except AirflowException as ae:
            if str(ae).startswith("404"):
                return False

            raise ae

        return True

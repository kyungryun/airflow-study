from datetime import datetime

from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator


class SlackAlert:
    def __init__(self, channel):
        slack_connection = BaseHook.get_connection(
            '')  # 해당 소스 호출 시, 적용할 connection명 연동 (ex. slack)
        self.slack_channel = channel
        self.slack_token = slack_connection.password  # webhook_url 토큰 저장

    def slack_fail_alert(self, context):
        alert = SlackWebhookOperator(
            task_id='slack_failed',
            http_conn_id='',  # http_conn_id 에 connection 명 저장
            channel=self.slack_channel,
            webhook_token=self.slack_token,  # webhook_token 에 webhook_url 저장
            proxy="",  # proxy 사전 세팅해야함
            message=
            """
:red_circle:
*Dag* : {dag}
*Task Failed* : {task}
*Execution Time*: {exec_date}
*Log Url*: {log_url}
            """.format(
                task=context.get('task_instance').task_id,
                dag=context.get('task_instance').dag_id,
                exec_date=context.get('execution_date'),
                log_url=context.get('task_instance').log_url,
            )
        )
        return alert.execute(context=context)

    def slack_success_alert(self, context, **kwargs):
        if {'task_id', 'task_title', 'task_result'} <= set(kwargs):
            result_title = context['ti'].xcom_pull(task_ids=kwargs["task_id"], key=kwargs["task_title"])
            result_message = context['ti'].xcom_pull(task_ids=kwargs["task_id"], key=kwargs["task_result"])
        else:
            result_title = '결과 없음'
            result_message = 0
            
        alert = SlackWebhookOperator(
            task_id='slack_succeed',
            http_conn_id='',  # http_conn_id 에 connection 명 저장
            channel=self.slack_channel,
            webhook_token=self.slack_token,  # webhook_token 에 webhook_url 저장
            proxy="",  # proxy 사전 세팅해야함
            message="""
:large_blue_circle:
*Dag* : {dag}
*Task Succeed* : {task}
*Execution Time*: {exec_date}
*Run Time* : {run_time}
*{result_title}* : {result_message}
*Log Url*: {log_url}
            """.format(
                task=context.get('task_instance').task_id,
                dag=context.get('task_instance').dag_id,
                exec_date=context.get('execution_date'),
                run_time=datetime.now(),
                result_title=result_title,
                result_message=result_message,
                log_url=context.get('task_instance').log_url
            )
        )
        return alert.execute(context=context)

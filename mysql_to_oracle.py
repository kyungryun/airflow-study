from airflow.hooks.oracle_hook import OracleHook
from airflow.hooks.mysql_hook import MySqlHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class MySqlToOracleOperator(BaseOperator):
    """
    :param sql                 : Execute Query MySQL
    :param mysql_table         : Source Table
    :param oracle_table        : Target Table
    :param mysql_conn_id       : Source Mysql Connection
    :param oracle_conn_id      : Target Oracle Connection
    :param oracle_commit_every : One transaction in Oracle
    """
    template_fields = ['sql', 'mysql_table', 'oracle_table']
    @apply_defaults
    def __init__(
            self,
            sql,
            mysql_table,
            oracle_table,
            mysql_conn_id='mysql_default',
            oracle_conn_id='oracle_default',
            oracle_commit_every=1000,
            *args, **kwargs):
        super(MySqlToOracleOperator, self).__init__(*args, **kwargs)
        self.sql = sql
        self.mysql_table = mysql_table
        self.oracle_table = oracle_table
        self.mysql_conn_id = mysql_conn_id
        self.oracle_conn_id = oracle_conn_id
        self.oracle_commit_every = oracle_commit_every
    def execute(self, context):
        mysql = MySqlHook(mysql_conn_id=self.mysql_conn_id)
        conn = mysql.get_conn()
        self.log.info("Extracting data from MySQL: %s", self.sql)

        cursor = conn.cursor()
        cursor.execute(self.sql)
        results = cursor.fetchall()

        oracle = OracleHook(oracle_conn_id=self.oracle_conn_id)
        self.log.info("Inserting rows into Oracle")
        oracle.insert_rows(table=self.oracle_table, rows=results, commit_every=self.oracle_commit_every)

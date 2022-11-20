from prometheus_api_client import PrometheusConnect
import json
from pprint import pprint

def get_query_summarised_result(url, query):
    prom = PrometheusConnect(url=url, disable_ssl=True)
    result = prom.custom_query(query=query)
    total_query_metrics = 0
    for metric in result:
        total_query_metrics += float(metric['value'][1])
    return total_query_metrics


if __name__ == '__main__':
    pprint(get_query_summarised_result(url='http://127.0.0.1:9090', query="sum(prometheus_http_requests_total)"))
from diagrams import Cluster, Diagram, Edge
from diagrams.aws.network import Endpoint
from diagrams.c4 import Container
from diagrams.onprem.database import ClickHouse
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram(
    "UGC Service", show=False, direction="TB", graph_attr={"splines": "spline"}
):
    gateway = Nginx("API Gateway")
    with Cluster("API"):
        endpoint = Endpoint("Endpoint")
        token_validator = Container(
            "Token Validator", description="Validate token signature"
        )
        payload_serializer = Container(
            "Payload Serializer", description="Validate and serialize data"
        )
        api_kafka = Container("Kafka Producer")

    kafka = Kafka("UGC Storage")

    with Cluster("UGC ETL"):
        etl_kafka = Container("Kafka Consumer")
        data_transformer = Container(
            "Transformer", description="Prepare data before loading"
        )
        etl_olap = Container("OLAP Connector")

    olap = ClickHouse("OLAP DB")

    gateway >> Edge(label="Incoming packet") >> endpoint

    endpoint >> token_validator
    endpoint >> payload_serializer >> api_kafka >> kafka

    kafka >> etl_kafka >> data_transformer >> etl_olap >> olap

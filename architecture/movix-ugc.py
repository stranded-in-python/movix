from diagrams import Cluster, Diagram, Edge
from diagrams.aws.network import Endpoint
from diagrams.c4 import Container, Database, Relationship, SystemBoundary
from diagrams.onprem.database import ClickHouse
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("UGC Service", show=False, direction="TB"):
    gateway = Nginx("API Gateway")
    with Cluster("API"):
        endpoint = Endpoint("Endpoint")
        with SystemBoundary("Authentication & Authorization"):
            token_validator = Container(
                "TokenValidator", description="Validate token signature"
            )
            access_checker = Container(
                "AccessChecker", description="Retrieve rights list from DB and check"
            )
        payload_serializer = Container(
            "PayloadSerializer", description="Validate and serialize data"
        )

    kafka = Kafka("UGC Storage")

    with Cluster("UGC ETL"):
        etl_kafka = Container("KafkaConnector")
        data_transformer = Container(
            "Transformer", description="Prepare data before loading"
        )
        etl_olap = Container("OLAP Connector")

    olap = ClickHouse("OLAP DB")

    gateway >> Edge(label="Incoming packet") >> endpoint

    access_checker >> token_validator
    access_checker << kafka
    endpoint >> access_checker >> payload_serializer >> kafka

    kafka >> etl_kafka >> data_transformer >> etl_olap >> olap

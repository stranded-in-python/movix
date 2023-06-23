from diagrams import Cluster, Diagram, Edge
from diagrams.c4 import Container, Relationship, SystemBoundary
from diagrams.elastic.saas import Elastic
from diagrams.generic.device import Mobile
from diagrams.generic.network import Switch
from diagrams.onprem.client import Client
from diagrams.onprem.database import ClickHouse, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.tracing import Jaeger
from diagrams.programming.language import Python

graph_attr = {
    "splines": "spline",
}

with Diagram(
    "Containers compose diagram Movix - To Be",
    show=False,
    outformat="png",
    graph_attr=graph_attr,
    direction="TB",
):
    client = Mobile("Client")
    admin = Client("Admin")

    with SystemBoundary("API gateway"):
        with Cluster("Tracing system"):
            tracing = Jaeger("Jaeger")

        with Cluster("API gateway"):
            ingress = Nginx("Nginx")
            circuit_breacker = Switch("Circuit Breaker")

        api = Container(
            name="Async API Application",
            technology="Python and FastAPI",
            description="Provides content for movies, genres, and persons.",
        )
        auth = Container(
            name="User Authentication Service",
            technology="Python and FastAPI",
            description="Provides a secure and reliable solution for user authentication and identity management.",
        )
        admin_panel = Container(
            name="Admin Panel Application",
            technology="Python and Django",
            description="Provides a user-friendly interface for managing and controlling content.",
        )

        ugc = Container(
            name="User Generated Content Service",
            technology="Python and FastAPI",
            description="An API for pushing users actions to storage",
        )

        with Cluster("ETL component"):
            etl = Python("Python Application")

        with Cluster("Cache Storage"):
            redis = Redis("Redis Cluster")

        with Cluster("Database"):
            user_schema = PostgreSQL("User Schema")
            content_schema = PostgreSQL("Content Schema")

        with Cluster("UGC Storage"):
            ugc_storage = Kafka("UGC Storage")

        with Cluster("OLAP Storage"):
            olap_storage = ClickHouse("OLAP Storage")

        with Cluster("Search Engine"):
            elastic = Elastic("AsyncElasticSearch")

    client >> Edge(color="darkgreen") << ingress
    ingress >> Edge(color="darkgreen") << api

    admin >> Edge(color="darkorange") << ingress
    ingress >> Edge(color="darkorange") << admin_panel

    ingress >> Edge(color="black", style="bold") << auth
    ingress >> Edge(color="black", style="bold") << ugc

    api >> Relationship() >> elastic
    api >> Relationship() >> redis
    api >> Relationship("Authorizing") >> ugc_storage

    auth >> Relationship("CRUD") >> user_schema
    auth >> Relationship("Update Rights topic") >> ugc_storage
    auth >> Relationship() >> redis
    auth >> Relationship() >> tracing

    ugc << Relationship("Authorizing") << ugc_storage
    ugc >> Relationship() >> ugc_storage
    ugc >> Relationship() >> olap_storage

    admin_panel >> Relationship("CRUD") >> content_schema

    user_schema >> Relationship("Extract") >> etl
    etl >> Relationship("Load") >> elastic

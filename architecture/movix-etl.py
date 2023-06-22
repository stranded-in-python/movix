from diagrams import Diagram
from diagrams.c4 import Container, Database, Relationship, SystemBoundary


with Diagram("Диаграмма ETL процесса", filename="movix-etl", direction="TB"):
    postgres = Database("Postgres")
    redis = Database("Redis")
    elastic_search = Database("ElasticSearch")

    with SystemBoundary("Extraction Manager"):
        postgres_producer = Container("PostgresProducer")
        enricher_manager = Container("EnricherManager")
        postgres_merger = Container("PostgresMerger")
        transformer = Container("Transformer")
        elastic_loader = Container("ElasticLoader")

        with SystemBoundary("State"):
            redis_storage = Container("RedisStorage")
            get_state = Container("get_state")
            set_state = Container("set_state")

    postgres_producer << Relationship("Считать указатель загруженного состояния") << get_state
    postgres_producer << Relationship("Список идентификаторов обновленных записей") << postgres
    postgres_producer >> Relationship("Записи на выгрузку") >> enricher_manager

    enricher_manager << Relationship("Записи на выгрузку") << postgres
    enricher_manager >> Relationship("Выгружаемый батч") >> postgres_merger

    postgres_merger >> Relationship("Обогащенные данные") >> transformer

    transformer >> Relationship("Трансляция в ElasticSearch QL") >> elastic_loader

    elastic_loader >> Relationship("Объекты в индекс") >> elastic_search
    elastic_loader >> Relationship("Сохранить указатель загруженного состояния") >> set_state

    set_state >> Relationship() >> redis_storage
    get_state << Relationship() << redis_storage

    redis_storage << Relationship("Считать/сохранить состояние", fontsize="20") >> redis

import sys
from threading import Thread
from multiprocessing import Process

from clickhouse_driver import Client
from datetime import datetime as dt

sys.path.append("..")
from utils import generate_random_data, timing


class ClickHouseTester:
    def __init__(self, clickhouse: Client = Client(host="localhost")):
        self.ch = clickhouse
        self.ch2 = Client(host="localhost")
        self.batch_size = 1000
        self.rows_number = 10_000_000

    def _before_testing(self):
        self.ch.execute("CREATE DATABASE IF NOT EXISTS test_db ON CLUSTER company_cluster")
        self.ch.execute("""
        CREATE TABLE IF NOT EXISTS test_db.regular_table ON CLUSTER company_cluster 
        (id Int64, user_id Int64, film_id Int64, timestamp DateTime64)
        Engine=MergeTree() ORDER BY id
        """)

    def _after_testing(self):
        self.ch.execute(
            "DROP DATABASE IF EXISTS test_db ON CLUSTER company_cluster"
        )

    def test(self):
        self._before_testing()
        print("--Write--")
        self.check_write(self.ch)
        print("--Read--")
        self.check_read(self.ch2)
        print("--Read And Write While Write--")
        self.check_read_while_write()
        self._after_testing()

    @timing
    def check_write(self, ch: Client):
        for batch in generate_random_data():
            ch.execute(
                "INSERT INTO test_db.regular_table (id, user_id, film_id, timestamp) VALUES",
                batch
            )
    
    def just_write(self, ch: Client):
        for batch in generate_random_data():
            ch.execute(
                "INSERT INTO test_db.regular_table (id, user_id, film_id, timestamp) VALUES",
                batch
            )

    def _check_read_while_write(self):
        self.check_read(self.ch)
        self.check_write(self.ch)
        
    @timing
    def check_read(self, ch: Client):
        data = ch.execute("SELECT * from test_db.regular_table")[0]
        print("Selected %s rows" % self.rows_number)
        print("Sample Data: %s" % [str(col) for col in data])

    @timing
    def check_read_while_write(self):
        noise = Process(target=self.just_write, args=(self.ch2,))
        test = Process(target=self._check_read_while_write)
        noise.start()
        test.start()
        noise.join()
        test.join()


if __name__=="__main__":
    tester = ClickHouseTester()
    tester.test()

# Output
# --Write--
# func:'check_write' took: 207.7547 sec
# --Read--
# Selected 10000000 rows
# Sample Data: ['12881', '1006344430', '4885477888', '2003-11-08 03:05:01']
# func:'check_read' took: 10.0420 sec
# --Read And Write While Write--
# Selected 10000000 rows
# Sample Data: ['6385997107', '7297643455', '2065710464', '2009-12-05 10:58:57']
# func:'check_read' took: 11.3118 sec
# func:'check_write' took: 217.9980 sec
# func:'check_read_while_write' took: 229.3303 sec
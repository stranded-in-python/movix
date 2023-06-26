import sys
from threading import Thread
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
        print("--Read While Write--")
        self.check_read_while_write()
        self._after_testing()

    @timing
    def check_write(self, ch: Client):
        for batch in generate_random_data():
            ch.execute(
                "INSERT INTO test_db.regular_table (id, user_id, film_id, timestamp) VALUES",
                batch
            )

    @timing
    def check_read(self, ch: Client):
        data = ch.execute("SELECT * from test_db.regular_table")[0]
        print("Selected %s rows" % self.rows_number)
        print("Sample Data: %s" % [str(col) for col in data])

    @timing
    def check_read_while_write(self): # не вижу смысла делать write_while_read
        t1 = Thread(target=self.check_write, args=(self.ch,))
        t2 = Thread(target=self.check_read, args=(self.ch2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


if __name__=="__main__":
    tester = ClickHouseTester()
    tester.test()

# Output
# --Write--
# func:'check_write' took: 211.6373 sec
# --Read--
# Selected 10000000 rows
# Sample Data: ['4608', '247037609', '1472547859', '2006-09-23 17:03:51']
# func:'check_read' took: 10.2997 sec
# --Read While Write--
# Selected 10000000 rows
# Sample Data: ['4608', '247037609', '1472547859', '2006-09-23 17:03:51']
# func:'check_read' took: 13.4429 sec
# func:'check_write' took: 224.8991 sec
# func:'check_read_while_write' took: 224.9004 sec
from typing import List, Dict, Optional, Any
import pytest
import enum
from dataclasses import dataclass

"""
sql: Memory db, insert, query, 
where filter, order by. 
select(table_name, where=None, order_by=None), only and is supported in the case of multiple where. Query with where condition. Query with where condition on multiple columns. Query with where condition and order by one column. Query with where condition and order by multiple columns

"""

class WhereClauseEnum(enum.Enum):
    """
    GT is the column value is greater than than given value
    """
    GREATER_THAN = 0
    LESSER_THAN = 1
    EQUALS = 2


@dataclass
class WhereClause:
    comparator: WhereClauseEnum
    field: str
    value: Any

    def record_is_included(self, entry: Dict) -> bool:
        if self.field in entry.keys():
            if self.comparator == WhereClauseEnum.GREATER_THAN:
                if not entry[self.field] > self.value:
                    return False
            elif self.comparator == WhereClauseEnum.LESSER_THAN:
                if not entry[self.field] < self.value:
                    return False
            elif self.comparator == WhereClauseEnum.EQUALS:
                if not entry[self.field] == self.value:
                    return False
            else:
                raise ValueError(F"Unsupported where clause comparator: {self.comparator}")
        else:
            raise ValueError(f"Field in where clause missing from record: {self.field}")        
        
        return True


class OrderClauseEnum(enum.Enum):
    ASCENDING = 0
    DESCENDING = 1


@dataclass
class OrderClause:
    order: OrderClauseEnum
    field: str


class SqlDb:

    def __init__(self):
        # table_name -> List[Dict]
        self.db: Dict[str, List[Dict]] = dict()

    def insert(self, table_name: str, data: Dict):
        if table_name not in self.db.keys():
            self.db[table_name] = list()
        
        self.db[table_name].append(data)

    def query(self, table_name : str, fields: List[str], 
              where: Optional[List[WhereClause]] = None, 
              order: Optional[OrderClause] = None):
        results: List[Dict] = list()

        for entry in self.db.get(table_name, list()):
            return_record = dict()

            if type(where) == list:
                if not all(w.record_is_included(entry) for w in where):
                    continue
                # handle all the wheres
            elif type(where) == WhereClause:
                if not where.record_is_included(entry):
                    continue
            # else it's None

            for key, value in entry.items():
                if key in fields:
                    return_record[key] = value
            
            if len(return_record.keys()) > 0:
                results.append(return_record)

        if order:
            if not all(order.field in entry.keys() for entry in results):
                raise ValueError(f"order by field must be present in all filtered results")
            
            if order.order == OrderClauseEnum.ASCENDING:
                return sorted(
                    (result for result in results), 
                    key=lambda x: x[order.field]
                    )
            elif order.order == OrderClauseEnum.DESCENDING:
                return sorted(
                    (result for result in results), 
                    key=lambda x: x[order.field], 
                    reverse=True
                    )
            else:
                raise ValueError(f"unsupported order direction: {order.order}")
        else:
            return results
    

@pytest.fixture
def sample_db() -> SqlDb:
    db = SqlDb()

    db.db = {
        "people" : [
            {
                "name" : "frank",
                "age" : 14
            },
            {
                "name" : "amy",
                "age" : 30,
                "country" : "Canada"
            }
        ]
    }

    return db

def test_query_column_exists(sample_db: SqlDb):
    assert sample_db.query("people", ["name"]) == [
        {
            "name" : "frank",
        },
        {
            "name" : "amy"
        }
    ]

def test_query_colum_ne(sample_db: SqlDb):
    assert sample_db.query("people", ["zzz"]) == []

def test_query_table_ne(sample_db: SqlDb):
    assert sample_db.query("foobar", ["name"]) == []

def test_query_column_partial(sample_db : SqlDb):
    assert sample_db.query("people", ["country"]) == [
        {
            "country" : "Canada"
        }
    ]

def test_query_where_gt_include(sample_db : SqlDb):
    where = WhereClause(
        comparator=WhereClauseEnum.GREATER_THAN,
        field="age",
        value=10)
    
    assert sample_db.query("people", ["name", "age"], where) == [
            {
                "name" : "frank",
                "age" : 14
            },
            {
                "name" : "amy",
                "age" : 30
            }
    ]

def test_query_where_gt_not_include(sample_db : SqlDb):
    where = WhereClause(
        comparator=WhereClauseEnum.GREATER_THAN,
        field="age",
        value=20)

    assert sample_db.query("people", ["name", "age"], where) == [
            {
                "name" : "amy",
                "age" : 30
            }
    ]

def test_query_where_lt(sample_db : SqlDb):
    where = WhereClause(
        comparator=WhereClauseEnum.LESSER_THAN,
        field="age",
        value=50)
    
    assert sample_db.query("people", ["name", "age"], where) == [
            {
                "name" : "frank",
                "age" : 14
            },
            {
                "name" : "amy",
                "age" : 30
            }
    ]

def test_query_where_eq(sample_db : SqlDb):
    where = WhereClause(
        comparator=WhereClauseEnum.EQUALS,
        field="age",
        value=14)
    
    assert sample_db.query("people", ["name", "age"], where) == [
            {
                "name" : "frank",
                "age" : 14
            }
    ]

def test_query_where_ne(sample_db : SqlDb):
    where = WhereClause(
        comparator=WhereClauseEnum.GREATER_THAN,
        field="zzz",
        value=10)

    with pytest.raises(ValueError):
        sample_db.query("people", ["name", "age"], where)

def test_query_order_asc(sample_db : SqlDb):
    order: OrderClause = OrderClause(
        order=OrderClauseEnum.ASCENDING,
        field="age"
    )

    assert sample_db.query("people", ["name", "age"], None, order) == [
                        {
                            "name" : "frank",
                            "age" : 14
                        },
                        {
                            "name" : "amy",
                            "age" : 30
                        }
                    ]

def test_query_order_desc(sample_db : SqlDb):
    order: OrderClause = OrderClause(
        order=OrderClauseEnum.DESCENDING,
        field="age"
    )

    assert sample_db.query("people", ["name", "age"], None, order) == [
                        {
                            "name" : "amy",
                            "age" : 30
                        },
                        {
                            "name" : "frank",
                            "age" : 14
                        },
                    ]

def test_query_order_ne(sample_db : SqlDb):
    order: OrderClause = OrderClause(
        order=OrderClauseEnum.DESCENDING,
        field="zzz"
    )

    with pytest.raises(ValueError):
        assert sample_db.query("people", ["name", "age"], None, order) == [
                            {
                                "name" : "amy",
                                "age" : 30
                            },
                            {
                                "name" : "frank",
                                "age" : 14
                            },
                        ]

def test_query_where_order(sample_db : SqlDb):
    sample_db.db["people"].append(
        {
            "name" : "leif",
            "age" : 33,
            "country" : "Canada"
        }
    )

    where = WhereClause(
        comparator=WhereClauseEnum.GREATER_THAN,
        field="age",
        value=15)
        
    order: OrderClause = OrderClause(
        order=OrderClauseEnum.DESCENDING,
        field="age"
    )

    assert sample_db.query("people", ["name", "age", "country"], where, order) == [
                        {
                            "name" : "leif",
                            "age" : 33,
                            "country" : "Canada"
                        },                        
                        {
                            "name" : "amy",
                            "age" : 30,
                            "country" : "Canada"
                        },
                    ]

def test_query_where_multi(sample_db: SqlDb):
    where_list = [
        WhereClause(
            comparator=WhereClauseEnum.EQUALS,
            field="age",
            value=14
        ),
        WhereClause(
            comparator=WhereClauseEnum.EQUALS,
            field="name",
            value="frank"
        )
    ]
    
    assert sample_db.query("people", ["name", "age"], where_list) == [
            {
                "name" : "frank",
                "age" : 14
            }
    ]    


if __name__ == "__main__":
    pytest.main(["openai/sql_db/sql_db.py"])
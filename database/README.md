# Database Scripts

The API depends on data that has been extracted, loaded, and transformed from the remote Heurist server into a simple DuckDB database file.

While it is possible to query the loaded database file using SQL, the LostMa data is heavily networked. As such, it is well suited to a graph database structure and certain queries are easier to manage using the graph querying langauge Cypher than the relational language SQL.

Therefore, tables in the DuckDB database file are transformed into nodes and edges in a Kùzu graph database.

## API's Session Dependencies

The API depends on a read-only connection to the Kùzu graph database. (See the [`GraphSessionDep`](../app/api/deps.py) context.)

Therefore, as the API starts up, it first checks to see that the Kùzu graph database has been created.

If the database is not found, the API runs the script in [`src/init_db.py`](./src/init_db.py), which (i) reloads fresh data from the Heurist server, (ii) writes it to a DuckDB database file, and (iii) builds a new Kùzu graph database from the latter's transformation.

After the databases have been created (Kùzu and DuckDB), the API starts its server and the entry points become available.

## Relational DB to Graph DB

Not everything in the Heurist database is meant to be made public in the API, and therefore does not need to be modelled in the graph transformation. However, the DuckDB process downloads everything that is in Heurist.

The relational-to-graph transformation modelling gives us an opportunity to refine the data to its finalised form, that which we want the public to access.

### Tables to Nodes

In [`graph_nodes.py`](./src/graph_nodes.py), select the columns that belong to the finalised node / object, rename them according to how you want, and affirm what data type they'll have in the Kùzu graph database.

```python
class Storyverse(Base):
    fields = [
        Field(column="H-ID", alias="id", type="INT64"),
        Field(column="preferred_name", alias="name", type="STRING"),
        Field(column="alternative_names", type="STRING[]"),
        Field(column="described_at_URL", alias="urls", type="STRING[]"),
    ]

    _from = """FROM Storyverse"""

    def __init__(self, conn: DuckDBPyConnection):
        self.conn = conn
```

The nodes are built from a base, which has methods to construct the full SQL needed to request all the desired data from the table / tables. Where in the relational database the data comes from is provided (in SQL) in the `_from` attribute. Finally, the nodes' data fields take a list of `Field` dataclasses. The custom `Field` dataclass takes the following input:

- `column` [required] : the SQL needed to select the data, i.e. the column name or a clause ("case when ..." or "unnest(...)").

- `alias` [optional] : the name of the data field, as it will be used on the node in the Kùzu graph database, if different than that used to select it in `column`.

- `type` [required] : the data type for that field on the Kùzu node.


### Foreign Keys to Edges

In [`graph_edges.py`](./src/graph_edges.py), select the primary key and foreign key of a table (the _from_ node).

Because edges can connect multiple types of nodes, it's necessary to make the pairs of _from_ and _to_ nodes into a list (`edges`) and to put the SQL needed to select their data into a list of the same length. The list of edges is composed of a list of custom `Edge` dataclasses, in which are given the _from_ node and _to_ node, i.e. `Edge("Witness", "Part")`.

Lastly, edges can have attributes (`_attr`) of their own, i.e. the attribute `lrm` (Library Reference Model relationship identifier).

```python
class IsMaterializedOn(Base):
    edges = [Edge("Witness", "Part"), Edge("Part", "Document")]
    _attr = "lrm"

    selections = [
        """
SELECT
    "H-ID" AS "from",
    unnest("observed_on_pages H-ID") AS "to",
    'R7' AS lrm
FROM Witness
WHERE "observed_on_pages H-ID" != []
""",
        """
SELECT
    "H-ID" AS "from",
    "is_inscribed_on H-ID" AS "to",
    'R7' AS lrm
FROM Part
WHERE "to" IS NOT NULL
""",
    ]
```

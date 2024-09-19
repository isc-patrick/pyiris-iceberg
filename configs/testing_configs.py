import os
import json 
import sys 

from dotenv import load_dotenv

load_dotenv()

base = {
    "job_type": "list_tables",
    "table_chunksize": 100000,
    "sql_clause": "",
    "table_name": "",
    "partition_field": "ID",
    "servers": [
        {
            "name": "LocalTesting",
            "dialect": "sqlite",
            "database": "/tmp/iceberg/test.db",
            "warehouse": "/tmp/iceberg",
            "connection_type": "sqlite",
            "schemas": [],
        },
        {
            "name": "LocalIRIS",
            "dialect": "iris",
            "database": "User",
            "driver": "com.intersystems.jdbc.IRISDriver",
            "host": "localhost",
            "password": "sys",
            "user": "_system",
            "port": 5551,
            "schemas": ["SQLUSER",],
            "connection_type": "db-api",
        }
    ],
    "icebergs": [
        {
            "name": "LocalTesting",
            "uri": "sqlite:////tmp/iceberg/pyiceberg_catalog.db",
            "warehouse": "/tmp/iceberg",
            "type": "sqlite",
        },
        {
            "name": "IRISCatalogLocalWarehouse",
            "uri": "iris://_SYSTEM:sys@localhost:5551/USER",
            "warehouse": "/tmp/iceberg",
            "type": "sqlite",
        }
    ] 
}

# No local data yet 
local_testing_config = {
    "src_server": "LocalTesting",
    "target_iceberg": "LocalTesting",
}

iris_src_local_target_config = {
    "src_server": "LocalIRIS",
    "target_iceberg": "IRISCatalogLocalWarehouse",
}


local_testing_config.update(base)
iris_src_local_target_config.update(base)

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
    
        if sys.argv[1] == "gen":
            configs = [k for k,v in locals().items() if k.endswith("_config")]
            for c in configs:
                json.dump(locals()[c], open(f'./configs/{c}' + ".json", "w"), indent=2)

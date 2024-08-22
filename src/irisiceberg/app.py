import sys
import traceback
from loguru import logger

from irisiceberg.main import IcebergIRIS
from irisiceberg.utils import Configuration
import pyiceberg

def get_config(config_name: str):
    conf = getattr(testing_configs, config_name)

    if not conf:
        print(f"No config named {config_name}")
        exit()
    
    return Configuration(**conf)

def create_IRISIceberg(config: Configuration):

    ice = IcebergIRIS("test", config)
    ice.iris.create_engine()
    return ice 

def purge_table(tablename: str, config_name: str):
    
    config = get_config(config_name)
    ice = create_IRISIceberg(config)
    try:
        ice.iceberg.catalog.purge_table(tablename)
    except pyiceberg.exceptions.NoSuchTableError as ex:
        logger.error(f"Cannot purge table {tablename}:  {ex}")
        #logger.error(f"Cannot purge table {tablename} because it does not exist")
    
def initial_table_sync(tablename, config_name: str):

    config = get_config(config_name)
    ice = create_IRISIceberg(config)
    ice.initial_table_sync(tablename)

    # Show some of the data from the new table
    ice_table = ice.iceberg.load_table(tablename)
    data = ice_table.scan(limit=100).to_pandas()
    print(ice_table.properties)
    print(data)

def update_table(tablename, config_name: str, clause: str = ""):
    config = get_config(config_name)
    ice = create_IRISIceberg(config)
    ice.update_iceberg_table(config.table_name, config.sql_clause)

if __name__ == "__main__":

    import pytest
    pytest.main()
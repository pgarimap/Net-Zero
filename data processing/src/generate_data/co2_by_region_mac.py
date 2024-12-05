import gcamreader
import pandas as pd
import numpy as np
from src.consts import SSP2, SPA1, TOPICS
from src.utils import get_data, merge_pak2south_asia, write_csv


## get co2 emission by region for spa1 and ssp2

def get_co2_by_region(ssp_scenario):
    query_file = "/Users/pramish/Desktop/Codes/netzero/gcam_code/data/mac_curve.xml"
    queries = gcamreader.parse_batch_query(query_file)
    query = queries[0]  # single query


    scenarios = ['GCAM_SSP2']
    dbpath = "/Volumes/Samsung USB/gcam output/"
    dbfile = "database_spa1_2p6"


    # connect to database
    conn = gcamreader.LocalDBConn(dbpath, dbfile)
    res = conn.runQuery(query, scenarios=scenarios)

    return res

get_co2_by_region(SPA1)
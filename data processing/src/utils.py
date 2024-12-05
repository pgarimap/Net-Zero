import os
from os import path as ospath
from os.path import join, exists

import pandas as pd
import xml.etree.ElementTree as ET

import gcamreader

from src.consts import SPA1, SSP2


def parse_rewrite(path):
    # parse the XML file
    tree = ET.parse(path)

    # get the root element
    root = tree.getroot()

    map = []
    # iterate over the `rewrite` elements
    for rewrite in root.findall('rewrite'):
        from_, to_ = rewrite.attrib['from'], rewrite.attrib['to']
        # print the 'from' and 'to' attributes
        map.append((from_, to_))
    return map


REGIONS = ['India', 'South Asia', 'China', 'Pakistan', 'Brazil', 'Africa_Western']
DEVELOPED_REGIONS = ['USA', 'EU-15', 'Australia_NZ', 'Canada', 'South Korea', 'Russia', 'European Free Trade Association']
ALL_REGIONS = ['India', 'South Asia', 'China', 'Pakistan', 'Brazil', 'Africa_Western', 'USA', 'EU-15', 'Australia_NZ', 'Canada',
               'South Korea', 'Russia', 'European Free Trade Association', 'Africa_Eastern', 'Central America and the Caribbean'
               'Africa_Northern', 'Africa_Southern', 'Argentina', 'Colombia', 'Mexico', 'Middle East', 'South Africa', 'Southeast Asia']

def get_data(ssp_name, query_path, regions=REGIONS):
    if not os.path.exists(query_path):
        raise (f"Query file doesn't exits in path: {query_path}")

    queries = gcamreader.parse_batch_query(query_path)
    query = queries[0]  # single query

    if ssp_name == SPA1:
        scenarios = ['SPA1GCAM_SSP1']
        scenarios = ['SSP1GCAM_SSP1']
        dbpath = "/Users/pramish/Desktop/Codes/netzero/gcam-v6.0/output/"
        # dbfile = "database_basexdb_2p6"
        dbfile = "database_basexdb_ssp1_spa1"

    elif ssp_name == SSP2:
        scenarios = ['SSP2GCAM_SSP2']
        dbpath = "/Users/pramish/Desktop/Codes/netzero/gcam-v6.0/output"
        dbfile = "database_basexdb_ssp2"
    else:
        raise "No such ssp handled"

    assert os.path.exists(dbpath)

    # connect to database
    conn = gcamreader.LocalDBConn(dbpath, dbfile)
    if regions:
        res = conn.runQuery(query, scenarios=scenarios, regions=regions)
    else:
        res = conn.runQuery(query, scenarios=scenarios)

    return res


def merge_pak2south_asia_new(df):
    df = df.copy()
    # Step 1: Filter out rows corresponding to the "Pakistan" region
    pakistan_rows = df[df['region'] == 'Pakistan'].copy()

    # Step 2: For these rows, change the "region" to "South Asia"
    pakistan_rows['region'] = 'South Asia'

    # Step 3: Append these modified rows to the original dataframe
    df_merged = pd.concat([df, pakistan_rows], ignore_index=True)

    # Step 4: Group by the common fields (excluding 'value') and sum the 'value' column
    grouped_columns = [col for col in df_merged.columns if col != 'value']
    df_grouped = df_merged.groupby(grouped_columns).sum().reset_index()
    df_grouped = df_grouped[df_grouped['region'] != 'Pakistan']
    return df_grouped


def merge_pak2south_asia(res, category_column=None, on=None, rename=True):
    '''
    merge pakistan value into south asia
    :param res:
    :param category_column:
    :param on:
    :return:
    '''

    result = res.copy()
    if rename:
        result = rename_column(result, category_column)

    sa = result[result['region'] == 'South Asia']
    pak = result[result['region'] == 'Pakistan']
    if on is not None:
        sa_pak = pd.merge(sa, pak, on=on, how='left')
    else:
        sa_pak = pd.merge(sa, pak, on=['Year', category_column, 'scenario', 'Units'], how='left')
    sa_pak['value'] = sa_pak['value_x'] + sa_pak['value_y']
    sa_pak.rename(columns={'region_x': 'region'}, inplace=True)
    sa_pak.drop(columns=['value_x', 'value_y'], inplace=True)

    # Pakistan from result
    # result = result[result['region'] != 'South Asia']
    result = result[result['region'] != 'Pakistan']

    # merge with original result
    if on is not None:
        result = pd.merge(result, sa_pak, on=on, how='left')
    else:
        result = pd.merge(result, sa_pak, on=['Year', category_column, 'scenario', 'Units', 'region'], how='left')

    result.rename(columns={'value_x': 'value'}, inplace=True)
    result.rename(columns={'region_x': 'region'}, inplace=True)

    if 'region_y' in result.columns:
        result.drop(columns=['region_y', 'value_y'], inplace=True)
    if 'sector_x' in result.columns:
        result.rename(columns={'sector_x': 'sector'}, inplace=True)
    if 'region_x' in result.columns:
        result.rename(columns={'region_x': 'region'}, inplace=True)
    return result


def rename_column(result, col_name, xml_path='/Users/pramish/Desktop/Codes/netzero/gcam_code/data/rewrite.xml'):
    name_mapper = parse_rewrite(xml_path)
    keys = [key[0] for key in name_mapper]
    vals = [key[1] for key in name_mapper]
    result[col_name] = result[col_name].replace(keys, vals)
    return result


def write_csv(df, fname, topic):
    path = f"/Users/pramish/Desktop/Codes/netzero/net-zero-codes/data processing/data_out"
    if not exists(join(path, topic)):
        os.mkdir(join(path, topic))
    full_path = f"{path}/{topic}/{fname}.csv"
    df.to_csv(full_path)

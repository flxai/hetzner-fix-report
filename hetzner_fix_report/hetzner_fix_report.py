import sys
from decimal import Decimal

import numpy as np
import pandas as pd
import regex as re


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_server_type(server_type_str: str):
    """Check whether string is contained"""
    server_type_list = server_type_str.split(' ')
    if len(server_type_list) == 1:
        return server_type_str.lower()
    if server_type_list[0].lower() == 'server':
        return server_type_list[1].partition('-')[0]
    return 'unknown'


def regex_match(server_type_str, regex, ret_id=1):
    """Applies a regular expression and returns a match """
    m = re.match(regex, server_type_str)
    return np.NaN if m is None else m.group(ret_id)


def regex_search(server_type_str, regex, ret_id=1):
    """Applies a regular expression and returns a match """
    m = re.search(regex, server_type_str)
    return np.NaN if m is None else m.group(ret_id)


def hetzner_fix_report(csv_path):
    # Keys for originally fucked CSV
    df_keys = [
        'server_type_str',
        'comment',
        'date_from',
        'date_to',
        'quantity',
        'price',
        'price_net',
        'empty',
    ]

    # Keys' new order
    df_keys_reorder = ['server_id', 'name', 'project', 'type', 'quantity', 'usage_hours', 'price', 'price_max',
                       'price_net', 'price_gross', 'vat', 'date_from', 'date_to', 'is_backup', 'is_server', 'is_ceph']

    # Load originally fucked CSV
    df = pd.read_csv(csv_path, sep=',', names=df_keys, converters={
        'price': Decimal,
        'price_net': Decimal,
        'quantity': Decimal,
    })

    # Whether entry is backup
    df['is_backup'] = df.server_type_str.apply(lambda x: 'Backup' in x)

    # Wether entry is server instance
    df['is_server'] = df.server_type_str.apply(lambda x: 'Server' in x)

    # Wether entry uses Ceph
    df['is_ceph'] = df.server_type_str.apply(lambda x: 'ceph' in x)

    # Server types according to https://www.hetzner.de/cloud
    df['type'] = df.server_type_str.apply(get_server_type)

    # Hetzner's instance id
    df['server_id'] = df.comment.apply(lambda x: regex_match(x, r'.*#([0-9]+) ".*'))

    # Maximum price for hourly rated servers
    df['price_max'] = df.comment.apply(lambda x: regex_search(x,
                                       r'(?:period|Zeitraum).*?((?:€\s*[\d.]+)|(?:[\d,]+\s*€))'))
    df_price_max_mask = ~df.price_max.isna()
    df.loc[df_price_max_mask, 'price_max'] = \
        df.price_max.loc[df_price_max_mask].apply(lambda x: float(x.replace('€', '').replace(',', '.')))

    # Set server name
    df['name'] = df.comment.apply(lambda x: regex_match(x, r'.+"([^"]+)"'))
    df.loc[df['name'] == 'instance', 'name'] = np.nan

    # Usage in hours
    df['usage_hours'] = df.comment.apply(lambda x: regex_search(x, r'(?:Usage|Nutzung):.*?(\d+)\s*h'))

    # Drop unnecessary columns
    df.drop(['comment', 'server_type_str', 'empty'], axis=1, inplace=True)

    # VAT was previously extracted from PDF. It is not included in the CSV, so we currently just assume 19%.
    vat = Decimal(19)
    df['vat'] = vat / 100
    df['price_net'] = df.quantity * df.price
    df['price_gross'] = df.price_net * (1 + df.vat)

    # Collect individual server ids' string locations and map them to nearest previous project name
    df['project'] = np.nan
    for idx in df.index:
        df.loc[idx, 'project'] = regex_search(idx, r'Cloud Project "([^"]+)"')

    # Reorder columns
    df = df[df_keys_reorder]

    return df

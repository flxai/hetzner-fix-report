import re
import pdftotext

import numpy as np
import pandas as pd


def get_server_type(server_type_str):
    """Check wether string is contained"""
    server_type_list = server_type_str.split(' ')
    if len(server_type_list) < 2:
        if server_type_str == 'Backup':
            return 'backup'
        else:
            return 'unknown'
    return server_type_list[1].split('-')[0]


def apply_regex(server_type_str, regex, ret_id=1):
    """Applies a regular expression and returns a match """
    m = re.match(regex, server_type_str)
    return np.NaN if m is None else m.group(ret_id)


def hetzner_fix_report(csv_path, pdf_path):
    # Keys for originally fucked CSV
    df_keys = [
        'server_type_str',
        'comment',
        'day_from',
        'day_to',
        'quantity',
        'price',
        'price_netto',
        'empty',
    ]

    # Keys' new order
    df_keys_reorder = ['id', 'name', 'project', 'type', 'quantity', 'usage_hours', 'price', 'price_netto',
                       'price_max', 'day_from', 'day_to', 'is_backup', 'is_server', 'is_ceph']

    # Load originally fucked CSV
    df = pd.read_csv(csv_path, sep=',', names=df_keys)

    # Wether entry is backup
    df['is_backup'] = df.server_type_str.apply(lambda x: 'Backup' in x)

    # Wether entry is server instance
    df['is_server'] = df.server_type_str.apply(lambda x: 'Server' in x)

    # Wether entry uses Ceph
    df['is_ceph'] = df.server_type_str.apply(lambda x: 'ceph' in x)

    # Server types according to https://www.hetzner.de/cloud
    df['type'] = df.server_type_str.apply(get_server_type)

    # Hetzner's instance id
    df['id'] = df.comment.apply(lambda x: apply_regex(x, r'^#([0-9]+) ".*'))

    # Maximum price for hourly rated servers
    df['price_max'] = df.comment.apply(lambda x: apply_regex(x.replace('\n', ' '),
                                       r'.+Maximalpreis für diesen Zeitraum: ([0-9,]+) €.*'))
    df_price_max_mask = ~df.price_max.isna()
    df.loc[df_price_max_mask, 'price_max'] = \
        df.price_max.loc[df_price_max_mask].apply(lambda x: float(x.replace(',', '.')))

    # Set server name
    df['name'] = df.comment.apply(lambda x: apply_regex(x, r'.+"([^"]+)"'))
    df.loc[df['name'] == 'instance', 'name'] = np.nan

    # Usage in hours
    df['usage_hours'] = df.comment.apply(lambda x: apply_regex(x.replace('\n', ' '), r'.+Nutzung: ([0-9]+) h.+'))

    # Drop unnecessary columns
    df.drop(['comment', 'server_type_str', 'empty'], axis=1, inplace=True)

    # Combine with pdf to get project names
    with open(pdf_path, 'rb') as f:
        pdf = pdftotext.PDF(f)

    # Collect individual projects' names
    projects = []
    for page in pdf:
        projects += re.findall(r'Proje[ck]t "([^"]+)"', page)
    projects = np.array(projects)

    # Collect individual projects' string locations
    projects_loc = []
    for project in projects:
        for page in pdf:
            loc = page.find(project)
            if loc != -1:
                projects_loc.append(loc)
    projects_loc = np.array(projects_loc)

    # Collect individual server ids' string locations and map them to nearest previous project name
    df['project'] = np.nan
    id_loc = []
    for idx, i in df.id[df.id.notnull()].items():
        for page in pdf:
            loc = page.find(i)
            if loc == -1:
                continue
            id_loc.append(loc)
            diff_loc = projects_loc - loc
            project_name = projects[np.where(diff_loc > 0, diff_loc, np.inf).argmin()]
            df.loc[idx, 'project'] = project_name

    # Reorder columns
    df = df[df_keys_reorder]

    return df

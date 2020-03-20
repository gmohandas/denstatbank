mock_sub_resp_default = [{'id': '02',
                          'description': 'Population and elections',
                          'active': True,
                          'hasSubjects': True,
                          'subjects': []},
                         {'id': '05',
                          'description': 'Living conditions',
                          'active': True,
                          'hasSubjects': True,
                          'subjects': []},
                         ]

mock_sub_resp_2401 = [{'id': '2401',
                       'description': 'Population and population projections',
                       'active': True,
                       'hasSubjects': True,
                       'subjects': [{'id': '10021',
                                     'description': 'Population in Denmark',
                                     'active': True,
                                     'hasSubjects': False,
                                     'subjects': []},
                                    {'id': '10022',
                                     'description': 'Population projections',
                                     'active': True,
                                     'hasSubjects': False,
                                     'subjects': []}]}]


mock_tables_resp = [{'id': 'FOLK1A',
                     'text': 'Population at the first day of the quarter',
                     'unit': 'number',
                     'updated': '2020-02-11T08:00:00',
                     'firstPeriod': '2008Q1',
                     'latestPeriod': '2020Q1',
                     'active': True,
                     'variables': ['region', 'sex', 'age', 'marital status', 'time']},
                    {'id': 'FOLK1B',
                     'text': 'Population at the first day of the quarter',
                     'unit': 'number',
                     'updated': '2020-02-11T08:00:00',
                     'firstPeriod': '2008Q1',
                     'latestPeriod': '2020Q1',
                     'active': True,
                     'variables': ['region', 'sex', 'age', 'citizenship', 'time']}]


mock_tableinfo_resp = {'id': 'FOLK1A',
                       'text': 'Population at the first day of the quarter',
                       'description': 'Population at the first day of the quarter by region, sex, age, marital status and time',
                       'unit': 'number',
                       'suppressedDataValue': '0',
                       'updated': '2020-02-11T08:00:00',
                       'active': True,
                       'footnote': None,
                       'variables': [{'id': 'KØN',
                                      'text': 'sex',
                                      'elimination': True,
                                      'time': False,
                                      'values': [{'id': 'TOT', 'text': 'Total'},
                                                 {'id': '1', 'text': 'Men'},
                                                 {'id': '2', 'text': 'Women'}]}]}


mock_tableinfo_variable_resp = {'id': ['000', '1', '32', 'U', '2008K4'],
                                'text': ['All  Denmark', 'Men', '32 years', 'Never married', '2008Q4'],
                                'variable': ['region', 'sex', 'age', 'marital status', 'time']
                                }


mock_data_resp = {'dataset': {'dimension': {'ContentsCode': {'label': 'Indhold',
                                                             'category': {'index': {'FOLK1A': 0},
                                                                          'label': {'FOLK1A': 'Population at the first day of the quarter'},
                                                                          'unit': {'FOLK1A': {'base': 'number', 'decimals': 0}}}},
                                            'Tid': {'label': 'time',
                                                    'category': {'index': {'2020K1': 0}, 'label': {'2020K1': '2020Q1'}}},
                                            'id': ['ContentsCode', 'Tid'],
                                            'size': [1, 1],
                                            'role': {'metric': ['ContentsCode'], 'time': ['Tid']}},
                              'label': 'Population at the first day of the quarter by Indhold and time',
                              'source': 'Statistics Denmark',
                              'updated': '2020-02-11T07:00:00Z',
                              'value': [5822763]}}


mock_data_resp_to_df = {
    ' Population at the first day of the quarter by Indhold and time': [5822763]}


mock_data_resp_with_vars = {'dimension': {'KØN': {'label': 'sex',
                                                  'category': {'index': {'M': 0, 'K': 1},
                                                               'label': {'M': 'Men', 'K': 'Women'}}},
                                          'FODLAND': {'label': 'country of birth',
                                                      'category': {'index': {'5101': 0, '5104': 1},
                                                                   'label': {'5101': 'Greenland', '5104': 'Finland'}}},
                                          'ContentsCode': {'label': 'Indhold',
                                                           'category': {'index': {'BEF5': 0},
                                                                        'label': {'BEF5': 'Population 1. January'},
                                                                        'unit': {'BEF5': {'base': 'number', 'decimals': 0}}}},
                                          'Tid': {'label': 'time',
                                                  'category': {'index': {'2018': 0, '2019': 1},
                                                               'label': {'2018': '2018', '2019': '2019'}}},
                                          'id': ['KØN', 'FODLAND', 'ContentsCode', 'Tid'],
                                          'size': [2, 2, 1, 2],
                                          'role': {'geo': ['FODLAND'], 'metric': ['ContentsCode'], 'time': ['Tid']}},
                            'label': 'Population 1. January by sex, country of birth, Indhold and time',
                            'source': 'Statistics Denmark',
                            'updated': '2020-02-11T07:00:00Z',
                            'value': [7016, 7095, 1266, 1263, 9454, 9471, 2766, 2787]}


mock_codes = ['køn', 'tid', 'fodland']

import pandas as pd
import pytest
from denstatbank.denstatbank import StatBankClient
from denstatbank.utils import data_dict_to_df, add_list_to_dict
from .mock_responses import (
    mock_sub_resp_default,
    mock_sub_resp_2401,
    mock_tables_resp,
    mock_tableinfo_resp,
    mock_tableinfo_variable_resp,
    mock_data_resp,
    mock_data_resp_to_df,
    mock_data_resp_with_vars,
    mock_codes
)


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")


@pytest.fixture
def client():
    client = StatBankClient()
    return client


def test_base_request(client, monkeypatch):
    def mock_base_request(self, *args, **kwargs):
        return mock_tableinfo_resp
    monkeypatch.setattr(StatBankClient, "base_request", mock_base_request)
    r = client.base_request('data', lang='en')
    assert r == mock_tableinfo_resp


def test_get_subjects(client, monkeypatch):
    def mock_get_subjects(self, subjects=None, include_tables=False, recursive=False):
        if subjects is None:
            return mock_sub_resp_default
    monkeypatch.setattr(StatBankClient, "get_subjects", mock_get_subjects)
    r = client.get_subjects()
    assert isinstance(r, list)
    d = r[0]
    assert isinstance(d, dict)
    assert 'id' in d.keys()
    assert 'description' in d.keys()


def test_get_subjects_returns_specified_subject(client, monkeypatch):
    def mock_get_subjects(self, subjects=None, include_tables=False, recursive=False):
        if subjects[0] == '2401':
            return mock_sub_resp_2401
    monkeypatch.setattr(StatBankClient, "get_subjects", mock_get_subjects)
    r = client.get_subjects(subjects=['2401'])
    assert isinstance(r, list)
    d = r[0]
    assert isinstance(d, dict)
    assert d['id'] == '2401'


def test_get_tables_returns_dict(client, monkeypatch):
    def mock_get_tables(self, subjects=None, past_days=None, include_inactive=False, as_df=True):
        return mock_tables_resp
    monkeypatch.setattr(StatBankClient, "get_tables", mock_get_tables)
    r = client.get_tables(as_df=False)
    assert isinstance(r, list)
    d = r[0]
    assert isinstance(d, dict)
    assert 'id' in d.keys()
    assert 'text' in d.keys()
    assert 'unit' in d.keys()
    assert 'updated' in d.keys()
    assert 'firstPeriod' in d.keys()
    assert 'latestPeriod' in d.keys()
    assert 'active' in d.keys()
    assert 'variables' in d.keys()


def test_get_tables_returns_df(client, monkeypatch):
    def mock_get_tables(self, subjects=None, past_days=None, include_inactive=False, as_df=True):
        return pd.DataFrame(mock_tables_resp)
    monkeypatch.setattr(StatBankClient, "get_tables", mock_get_tables)
    df = client.get_tables()
    assert isinstance(df, pd.DataFrame)
    assert 'id' in df.columns
    assert 'text' in df.columns
    assert 'unit' in df.columns
    assert 'updated' in df.columns
    assert 'firstPeriod' in df.columns
    assert 'latestPeriod' in df.columns
    assert 'active' in df.columns
    assert 'variables' in df.columns


def test_get_tableinfo_returns_dict(client, monkeypatch):
    def mock_get_tableinfo(self, table_id, variables_df=False):
        return mock_tableinfo_resp
    monkeypatch.setattr(StatBankClient, "get_tableinfo", mock_get_tableinfo)
    d = client.get_tableinfo('FOLK1A')
    assert isinstance(d, dict)
    assert d['id'] == 'FOLK1A'
    assert 'id' in d['variables'][0].keys()
    assert 'text' in d['variables'][0].keys()


def test_get_tableinfo_returns_variables_df(client, monkeypatch):
    def mock_get_tableinfo(self, table_id, variables_df):
        if variables_df:
            return pd.DataFrame(mock_tableinfo_variable_resp)
    monkeypatch.setattr(StatBankClient, "get_tableinfo", mock_get_tableinfo)
    df = client.get_tableinfo('FOLK1A', variables_df=True)
    assert isinstance(df, pd.DataFrame)
    print(df)
    assert 'id' in df.columns
    assert 'text' in df.columns
    assert 'variable' in df.columns
    assert len(df.columns.tolist()) == 3


def test_get_data_returns_dict(client, monkeypatch):
    def mock_get_data(self, table_id, as_df, variables=None, **kwargs):
        return mock_data_resp
    monkeypatch.setattr(StatBankClient, "get_data", mock_get_data)
    d = client.get_data(table_id='folk1a', as_df=False)
    assert isinstance(d, dict)
    assert 'dataset' in d.keys()
    dd = d['dataset']
    assert 'value' in dd.keys()
    assert isinstance(dd['value'], list)


def test_get_data_returns_df(client, monkeypatch):
    def mock_get_data(self, table_id, as_df=True, variables=None, **kwargs):
        return pd.DataFrame(mock_data_resp_to_df)
    monkeypatch.setattr(StatBankClient, "get_data", mock_get_data)
    d = client.get_data(table_id='folk1a')
    assert isinstance(d, pd.DataFrame)


def test_make_variables_dict(client):
    kon = client.make_variable_dict(code='køn', values=['M', 'K'])
    assert isinstance(kon, dict)
    assert 'code' in kon.keys()
    assert 'values' in kon.keys()
    assert kon['code'] == 'køn'
    assert isinstance(kon['values'], list)
    assert kon['values'] == ['M', 'K']

    tid = client.make_variable_dict(code='tid', values='2018')
    assert isinstance(tid, dict)
    assert 'code' in tid.keys()
    assert 'values' in tid.keys()
    assert tid['code'] == 'tid'
    assert isinstance(tid['values'], list)
    assert tid['values'] == ['2018']


def test_data_dict_to_df():
    df = data_dict_to_df(mock_data_resp_with_vars, mock_codes)
    assert isinstance(df, pd.DataFrame)
    assert isinstance(df.index, pd.MultiIndex)
    assert df.shape == (8, 1)


def test_add_list_to_dict():
    params = {'lang': 'en'}
    add_list_to_dict(params, subjects=['02'])
    assert 'subjects' in params.keys()
    assert isinstance(params['subjects'], list)
    assert params['subjects'] == ['02']

    with pytest.raises(Exception) as e:
        assert add_list_to_dict(params, subjects='03')
    assert str(e.value) == 'subjects must be a list.'

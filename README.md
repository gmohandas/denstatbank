# denstatbank
![denstatbank](https://github.com/gmohandas/denstatbank/workflows/denstatbank/badge.svg)

A wrapper to Statistics Denmark's DataBank API.
The library allows you to easily retrieve data on a variety of topics made available by [Statistics Denmark](https://www.dst.dk/en) 

The package provides a simple interface for professional statisticians, academics, policymakers, students, 
and anyone interested in quantitative facts about Denmark.

### Installation

```
pip install denstatbank
```

### Usage

Quick Example 
```python
>>> from denstatbank import StatBankClient
>>> sbc = StatBankClient(lang='en')
>>> df = sbc.get_data(table_id='bef5')
>>> df
   Population 1. January by Indhold and time
0                                    5822763
```


### DataBank API
The official API documentation can be found [here](https://www.dst.dk/en/Statistik/statistikbanken/api)

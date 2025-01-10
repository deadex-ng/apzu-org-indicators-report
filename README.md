# Organisation Indicators Report

To compile the HIV data report follow these steps

1. Create a virtual environment

```python
python -m venv venv
```

2. Activate the environment

```python
source venv/bin/activate
```

3. Install packages

```python
pip install -r requirements.txt
```

4. create the report file.

```python
python3 utils/create_report.py  -p "./output/Upper Neno HIV-Data 2024.xlsx" -s Upper -t HIV
```

5. Check dates for the HIV and NCD queries in ./utils/hiv_queries.py and ./utils/ncd_queries.py. If you are satisfied with the dates, proceed to the next step.

6. Pull and write data to file

```python
python3 main.py -p "./output/Upper Neno HIV-Data 2024.xlsx" -s Upper
```

6. Check the `output` folder for the excel report

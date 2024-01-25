import pandas as pd
from sqlalchemy import create_engine

# driver://username:password@host:port/database
engine = create_engine('postgresql://postgres:Ugne13@localhost:5432/cvmarket_data')
sql_query = "SELECT * FROM it_jobs_data;"
dff = pd.read_sql_query(sql_query, engine)

print(dff)
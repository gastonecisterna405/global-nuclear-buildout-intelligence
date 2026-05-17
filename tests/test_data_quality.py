import pandas as pd
from src.data.data_quality_checks import run_data_quality_checks

def test_quality_smoke():
    r=pd.DataFrame({'reactor_id':['a'],'country':['X'],'source_name':['s'],'source_confidence':[.5]})
    c=pd.DataFrame({'country':['X']})
    assert run_data_quality_checks(r,c)['reactor_rows']==1

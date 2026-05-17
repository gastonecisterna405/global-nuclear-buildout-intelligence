from src.features.reactor_features import add_reactor_feature_flags
import pandas as pd

def test_flags():
    df=pd.DataFrame({'reactor_type_standardized':['MSR'],'technology_family':['Molten Salt Reactor']})
    assert add_reactor_feature_flags(df).loc[0,'molten_salt_flag']

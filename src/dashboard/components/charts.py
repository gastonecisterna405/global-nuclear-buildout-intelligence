import plotly.express as px

def bar(df, x, y, color=None, title=None):
    return px.bar(df, x=x, y=y, color=color, title=title, template="plotly_white")

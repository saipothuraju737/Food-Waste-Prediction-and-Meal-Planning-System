import numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
CAT=["day","meal"]; NUM=["special","nonveg","dessert","exam","festival"]; CAPACITY=350; KG_PER_MEAL=0.42
def make(est):
    return Pipeline([("p",ColumnTransformer([("c",OneHotEncoder(handle_unknown="ignore"),CAT),("n",StandardScaler(),NUM)])),("m",est)])
ALGOS={"Linear Regression":lambda:LinearRegression(),
 "Decision Tree":lambda:DecisionTreeRegressor(max_depth=6,random_state=1),
 "Random Forest":lambda:RandomForestRegressor(200,random_state=1),
 "Gradient Boosting":lambda:GradientBoostingRegressor(random_state=1),
 "KNN Regressor":lambda:KNeighborsRegressor(7)}
def train(csv="data/mess_log.csv"):
    df=pd.read_csv(csv,parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    cut=int(len(df)*.8); tr,te=df.iloc[:cut],df.iloc[cut:]   # time-based split: test = most recent 20%
    X,y=CAT+NUM,"served"; metrics=[]; preds={}
    for n,f in ALGOS.items():
        p=make(f()).fit(tr[X],tr[y]).predict(te[X]); preds[n]=p
        metrics.append({"model":n,"mae":round(mean_absolute_error(te[y],p),2),
          "rmse":round(float(np.sqrt(mean_squared_error(te[y],p))),2),"r2":round(r2_score(te[y],p),3)})
    best=min(metrics,key=lambda m:m["mae"]); bp=preds[best["model"]]
    sugg=np.minimum(CAPACITY,np.ceil(bp+1.28*best["rmse"]))   # ~90% safety margin
    back={"test_rows":len(te),"avg_prepared_now":round(float(te.prepared.mean()),1),
      "avg_leftover_now":round(float((te.prepared-te.served).clip(0).mean()),1),
      "avg_prepared_suggested":round(float(sugg.mean()),1),
      "avg_leftover_suggested":round(float(np.clip(sugg-te.served,0,None).mean()),1),
      "shortfall_pct":round(float((sugg<te.served).mean()*100),1),
      "note":"Back-test on held-out data only. Real savings must be measured in the pilot."}
    models={n:make(f()).fit(df[X],df[y]) for n,f in ALGOS.items()}
    return {"models":models,"metrics":metrics,"best":best["model"],"rmse":best["rmse"],"backtest":back,"rows":len(df)}

import math, pandas as pd
from datetime import datetime
from flask import Flask, jsonify, request
from menu import MENU, DAYS
import train as T
CSV="data/mess_log.csv"; app=Flask(__name__,static_folder="static",static_url_path="")
S=T.train()
@app.route("/")
def home(): return app.send_static_file("index.html")
@app.route("/api/menu")
def menu(): return jsonify({d:{m:dict(zip(["menu","special","nonveg","dessert"],v)) for m,v in x.items()} for d,x in MENU.items()})
@app.route("/api/metrics")
def metrics(): return jsonify({k:S[k] for k in ["metrics","best","backtest","rows"]})
@app.route("/api/stats")
def stats():
    df=pd.read_csv(CSV); g=df.groupby(["day","meal"]).served.mean().round().astype(int)
    return jsonify({d:{m:int(g[(d,m)]) for m in ["breakfast","lunch","dinner"]} for d in DAYS})
@app.route("/api/predict",methods=["POST"])
def predict():
    j=request.json; day=DAYS[datetime.strptime(j["date"],"%Y-%m-%d").weekday()]
    row=pd.DataFrame([{"day":day,"meal":j["meal"],"special":int(j["special"]),"nonveg":int(j["nonveg"]),
      "dessert":int(j["dessert"]),"exam":int(j["exam"]),"festival":int(j["festival"])}])
    allp={n:max(0,round(float(m.predict(row)[0]))) for n,m in S["models"].items()}
    name=j.get("model") or S["best"]; pred=allp[name]
    sug=min(T.CAPACITY,math.ceil(pred+1.28*S["rmse"])); cur=int(j.get("current",370))
    return jsonify({"day":day,"model":name,"predicted":pred,"suggested":sug,"current":cur,
      "extra_now":max(cur-sug,0),"kg_avoidable":round(max(cur-sug,0)*T.KG_PER_MEAL,1),"all":allp})
@app.route("/api/log",methods=["POST"])
def log():
    global S
    j=request.json; day=DAYS[datetime.strptime(j["date"],"%Y-%m-%d").weekday()]
    mn,sp,nv,ds=MENU[day][j["meal"]]; prep,srv=int(j["prepared"]),int(j["served"]); left=max(prep-srv,0)
    kg=float(j.get("leftover_kg") or round(left*T.KG_PER_MEAL,1))
    pd.DataFrame([[j["date"],day,j["meal"],mn,sp,nv,ds,int(j["exam"]),int(j["festival"]),prep,srv,left,kg]]).to_csv(CSV,mode="a",header=False,index=False)
    S=T.train(); return jsonify({"ok":True,"rows":S["rows"],"best":S["best"]})
if __name__=="__main__": app.run(debug=False,port=5000)

"""Creates data/students.csv (350 unique names) and data/mess_log.csv (daily records per meal).
NOTE: synthetic, built from the owner's description; replace with real logs when collected."""
import random, numpy as np, pandas as pd
from datetime import date, timedelta
from menu import MENU, DAYS
random.seed(7); np.random.seed(7)
FIRST="Aarav Aditya Akash Ananya Anil Ankita Arjun Ayush Bhavya Chaitanya Deepak Divya Gaurav Harsh Ishita Jyoti Kavya Kiran Lakshmi Manish Meera Mohit Nandini Naveen Neha Nikhil Pooja Pranav Priya Rahul Rakesh Rohan Sai Sanjana Saurav Shreya Siddharth Sneha Subham Sunil Suresh Tanvi Tejas Varun Vikram Vishal Yash Sourav Swati Rashmi Debasish Soumya Bibhu Smruti Lipsa Abhisek Biswajit Satyam Trisha Anjali Karthik Ravi Mahesh Venkat Sandeep".split()
LAST="Sahoo Mohanty Panda Patra Nayak Behera Das Mishra Rout Swain Jena Pradhan Reddy Sharma Kumar Singh Patel Naidu Verma Gupta Rao Dash Padhi Otta Samal Barik Mahapatra Tripathy".split()
combos=[f"{f} {l}" for f in FIRST for l in LAST]; random.shuffle(combos)
names=combos[:350]; assert len(set(names))==350
pd.DataFrame({"student_id":[f"IIIT{24000+i}" for i in range(350)],"name":names,
 "diet":np.random.choice(["Veg","Non-Veg"],350,p=[.35,.65]),
 "block":np.random.choice(["GF-A","GF-B","GF-C"],350)}).to_csv("data/students.csv",index=False)
EXAMS=[(date(2026,8,3),date(2026,8,14)),(date(2026,10,5),date(2026,10,16))]
FEST={date(2026,8,15),date(2026,8,28),date(2026,9,14),*[date(2026,10,d) for d in range(17,22)]}
BASE={"breakfast":.55,"lunch":.62,"dinner":.66}
rows=[]; d=date(2026,6,1)
while d<=date(2026,10,27):
    day=DAYS[d.weekday()]; ex=int(any(a<=d<=b for a,b in EXAMS)); fe=int(d in FEST)
    for meal in ["breakfast","lunch","dinner"]:
        menu,sp,nv,ds=MENU[day][meal]
        p=BASE[meal]+.06*sp+.05*nv+.03*ds+.14*ex+.12*fe+np.random.normal(0,.03)
        if day=="Sunday" and meal=="breakfast": p-=.06
        served=int(min(350,max(60,p*350)))
        prepared=random.randint(360,380)            # current practice: cook for ~370
        left=max(prepared-served,0)
        rows.append([d,day,meal,menu,sp,nv,ds,ex,fe,prepared,served,left,round(left*0.42*random.uniform(.9,1.1),1)])
    d+=timedelta(1)
pd.DataFrame(rows,columns=["date","day","meal","menu","special","nonveg","dessert","exam","festival",
 "prepared","served","leftover_meals","leftover_kg"]).to_csv("data/mess_log.csv",index=False)
print("students:",len(names),"records:",len(rows))

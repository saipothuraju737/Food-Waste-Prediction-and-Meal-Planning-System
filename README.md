# Mess Food Planner (IIIT Bhubaneswar Ground Floor Mess)
Predicts how many students will eat each meal (and how much to cook) to cut food waste.
## Run
    pip install -r requirements.txt
    python generate_data.py   # makes data/students.csv (350 unique names) + data/mess_log.csv
    python app.py             # open http://127.0.0.1:5000
## Models (train.py)
Linear Regression, Decision Tree, Random Forest, Gradient Boosting, KNN. Best by MAE on the latest 20% of days is used.
Suggested quantity = prediction + 1.28 x RMSE (about 90% safety margin), capped at 350.
## Real data
The dataset is SYNTHETIC (from the owner's description: ~250 normal day, more on specials, exams, festivals).
Replace data/mess_log.csv with real records (same columns) or use the "Log Actuals" tab daily in the pilot week.
Do not claim savings until measured with real before/after leftover weights.

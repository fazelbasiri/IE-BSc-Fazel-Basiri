from pulp import LpProblem, LpMinimize, lpSum, LpVariable

years = [1402, 1403, 1404, 1405]
categories= ['Skilled', 'Semi-Skilled', 'Entry-Level']
skilled_required = {1402: 1000, 1403: 1000, 1404: 1500, 1405: 2000}
semi_skilled_required = {1402: 1500, 1403: 1400, 1404: 2000, 1405: 2500}
entry_level_required = {1402: 2000, 1403: 1000, 1404: 500, 1405: 0}
recruitment_limit = {"Skilled": 500, "Semi-Skilled": 800, "Entry-Level": 500}
training_limit = {'First_type': 200, 'Second_type': 0.25}

training_cost = {'First_type': 4, 'Second_type': 5}
layoff_cost = {'Skilled': 30, 'Semi-Skilled': 20, 'Entry-Level': 15}
surplus_cost = {'Skilled': 6, 'Semi-Skilled': 5, 'Entry-Level': 4}
# New
leave_rate = {'Skilled': 0.15, 'Semi-Skilled': 0.2, 'Entry-Level': 0.25}

retention_due_to_welfare = {'Skilled': 150, 'Semi-Skilled': 200, 'Entry-Level': 200}
# in units of million tomans
welfare_increase_cost = 100

model = LpProblem(name="HR_Optimization", sense=LpMinimize)

X = {year: {category: LpVariable(name=f"X_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
Y = {year: {category: LpVariable(name=f"Y_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
W = {year: {training_type: LpVariable(name=f"W_{training_type}_{year}", lowBound=0, cat="Integer") for training_type in ['First_type', 'Second_type']} for year in years}
S = {year: {category: LpVariable(name=f"S_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
# New ; binary
L = {year: LpVariable(name=f"L_{year}", lowBound=0, cat="Binary") for year in years}
W1 = {year: {category: LpVariable(name=f"W1_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}

total_cost = lpSum(X[year][category] + W[year][training_type] + layoff_cost[category] * Y[year][category] + surplus_cost[category] * S[year][category]+ welfare_increase_cost * L[year] for year in years for category in categories for training_type in ['First_type', 'Second_type'])
model += total_cost

#Defining constraints 
for year in years  :  
    for category in categories:
        model += X[year][category] <= recruitment_limit[category]
        model += X[year][category] + S[year][category] - Y[year][category] == locals()[f"{category.replace('-', '_').lower()}_required"][year] - leave_rate[category] * X[year][category] + retention_due_to_welfare[category] * L[year]
   
    model += W1[year]['Skilled'] <= 200
    model += W1[year]['Semi-Skilled'] <= 200
    model += W1[year]['Entry-Level'] <= 200
   
    model += W[year]['Second_type'] <= 0.25 * X[year]['Skilled']

    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
        model += S[year][category] <= 50

    model += X[year]['Skilled'] + X[year]['Semi-Skilled'] + X[year]['Entry-Level'] >= recruitment_limit['Skilled'] * L[year]

model.solve()

print("\nResults:")
print("Status:", model.status)
print("Total Cost in unit of Million Tomans):", model.objective.value())

for year in years:
    print(f"\nResults for the year {year}:")
    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
        print(f"{category} Workforce:", X[year][category].value())
        print(f"First type Training in {category}:", W1[year][category].value())
from pulp import LpProblem, LpMinimize, LpVariable, lpSum
years = [1402, 1403, 1404, 1405]

# Number of manpowers per year for each category
skilled_required = {1402: 1000, 1403: 1000, 1404: 1500, 1405: 2000}
semi_skilled_required = {1402: 1500, 1403: 1400, 1404: 2000, 1405: 2500}
entry_level_required = {1402: 2000, 1403: 1000, 1404: 500, 1405: 0}

recruitment_limit = {'Skilled': 500, 'Semi-Skilled': 800, 'Entry-Level': 500}
training_limit = {'First_type': 200, 'Second_type': 0.25}

#Costs are in unit of Million Tomans
training_cost = {'First_type': 4, 'Second_type': 5}
layoff_cost = {'Skilled': 30, 'Semi-Skilled': 20, 'Entry-Level': 15}
surplus_cost = {'Skilled': 6, 'Semi-Skilled': 5, 'Entry-Level': 4}

model = LpProblem(name="HR_Optimization", sense=LpMinimize)

# Variables; X: number of required manpowers to hire,  Y: number of required manpowers to lay off,  W: number of required manpowers to train,  S: number of surplus manpower
X = {year: {category: LpVariable(name=f"X_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
Y = {year: {category: LpVariable(name=f"Y_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
W = {year: {training_type: LpVariable(name=f"W_{training_type}_{year}", lowBound=0, cat="Integer") for training_type in ['First_type', 'Second_type']} for year in years}
S = {year: {category: LpVariable(name=f"S_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}

# Objective function
total_cost = lpSum(X[year][category] + W[year][training_type] + layoff_cost[category] * Y[year][category] + surplus_cost[category] * S[year][category] for year in years for category in ['Skilled', 'Semi-Skilled', 'Entry-Level'] for training_type in ['First_type', 'Second_type'])

model += total_cost

# Constraints
for year in years:
    # Number of hired manpowers per year for each category
    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
         model += X[year][category] + S[year][category] - Y[year][category] == skilled_required[year] if category == 'Skilled' else \
          X[year][category] + S[year][category] - Y[year][category] == semi_skilled_required[year] if category == 'Semi-Skilled' else \
          X[year][category] + S[year][category] - Y[year][category] == entry_level_required[year]

    # Number of training courses
    model += W[year]['First_type'] <= training_limit['First_type']
    model += W[year]['Second_type'] <= 0.25 * X[year]['Skilled']

    # Additional recruitment
    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
        model += S[year][category] <= 50

model.solve()

print("\nResults:")
print("Status:", model.status)
print("Total Cost in unit of Million Tomans:", model.objective.value())

for year in years:
    print(f"\nResults for year of {year}:")
    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
        print(f"{category} Manpower:", X[year][category].value())
        print(f"First type Training in {category}:", W[year]['First_type'])
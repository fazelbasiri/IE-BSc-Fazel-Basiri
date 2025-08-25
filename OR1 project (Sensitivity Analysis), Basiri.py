from pulp import LpProblem, LpMinimize, lpSum, LpVariable
import matplotlib.pyplot as plt
years = [1402, 1403, 1404, 1405]

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

X = {year: {category: LpVariable(name=f"X_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
Y = {year: {category: LpVariable(name=f"Y_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}
W = {year: {training_type: LpVariable(name=f"W_{training_type}_{year}", lowBound=0, cat="Integer") for training_type in ['First_type', 'Second_type']} for year in years}
S = {year: {category: LpVariable(name=f"S_{category}_{year}", lowBound=0, cat="Integer") for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']} for year in years}

total_cost =lpSum(X[year][category] + W[year][training_type] + layoff_cost[category] * Y[year][category] + surplus_cost[category] * S[year][category] for year in years for category in ['Skilled', 'Semi-Skilled', 'Entry-Level'] for training_type in ['First_type', 'Second_type'])

model += total_cost

# Constraints
for year in years:
    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
         model += X[year][category] + S[year][category] - Y[year][category] == skilled_required[year] if category == 'Skilled' else \
          X[year][category] + S[year][category] - Y[year][category] == semi_skilled_required[year] if category == 'Semi-Skilled' else \
          X[year][category] + S[year][category] - Y[year][category] == entry_level_required[year]


    model += W[year]['First_type'] <= training_limit['First_type']
    model += W[year]['Second_type'] <= 0.25 * X[year]['Skilled']

    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
        model += S[year][category] <= 50

model.solve()

print("\nResults:")
print("Status:", model.status)
print("Total Cost in unit of Million Tomans:", model.objective.value())

for year in years:
    print(f"\nResults for the year {year}:")
    for category in ['Skilled', 'Semi-Skilled', 'Entry-Level']:
        print(f"{category} Manpower:", X[year][category].value())
        print(f"First type Training in {category}:", W[year]['First_type'])
    
    
# Analysis test:
param1_name = 'layoff_cost_skilled'
param2_name = 'training_limit_first_type'

# For the first one
param1_values = [10, 20, 30]
results_param1 = []

for param1_value in param1_values:
   
    layoff_cost['Skilled'] = param1_value

    model.solve()
    results_param1.append(model.objective.value())

# For the second one
param2_values = [150, 200, 250]
results_param2 = []


for param2_value in param2_values:
    training_limit['First_type'] = param2_value
    model.solve()
    results_param2.append(model.objective.value())

plt.figure(figsize=(10, 6))
plt.plot(param1_values, results_param1, marker='o', label=f'{param1_name} Sensitivity')
plt.plot(param2_values, results_param2, marker='o', label=f'{param2_name} Sensitivity')

plt.title('Sensitivity Analysis')
plt.xlabel('Parameter Values')
plt.ylabel('Total Cost in unit of Million Tomans')
plt.legend()
plt.grid(True)
plt.show()
import pandas as pd
import numpy as np
from collections import defaultdict

# ----------------------------------------------------------------------
# 1. Load and preprocess the data
# ----------------------------------------------------------------------
df = pd.read_csv('flights.csv', parse_dates=['date'])

# Extract all unique cities
cities = sorted(set(df['from']).union(df['to']))
num_cities = len(cities)
city_index = {city: i for i, city in enumerate(cities)}

# ----------------------------------------------------------------------
# 2. Attraction value per city = number of incoming flights (popularity)
# ----------------------------------------------------------------------
attraction = df['to'].value_counts().to_dict()
for c in cities:
    if c not in attraction:
        attraction[c] = 0
print("City attractions (incoming flights):")
for c, v in attraction.items():
    print(f"  {c}: {v}")

# ----------------------------------------------------------------------
# 3. Build a dictionary of round‑trip flight costs
# ----------------------------------------------------------------------
# cost_matrix[(from, to)] = average one‑way price
pair_prices = df.groupby(['from', 'to'])['price'].mean().to_dict()

def get_round_trip_cost(origin, destination):
    """Estimate round‑trip cost using historical data; fallback to distance‑based."""
    leg1 = pair_prices.get((origin, destination), None)
    leg2 = pair_prices.get((destination, origin), None)
    if leg1 is not None and leg2 is not None:
        return leg1 + leg2
    if leg1 is not None:
        return 2.0 * leg1   # assume return same price
    if leg2 is not None:
        return 2.0 * leg2
    # if no direct data, use median cost per km from all flights
    df_temp = df.copy()
    df_temp['cost_per_km'] = df_temp['price'] / df_temp['distance']
    median_cpk = df_temp['cost_per_km'].median()
    # get distance for this pair (any flight between these cities)
    dist_rows = df[(df['from'] == origin) & (df['to'] == destination)]
    if dist_rows.empty:
        dist_rows = df[(df['from'] == destination) & (df['to'] == origin)]
    if not dist_rows.empty:
        dist = dist_rows['distance'].iloc[0]
    else:
        # approximate distance as the mean distance between all city pairs
        dist = df['distance'].mean()
    return 2.0 * median_cpk * dist

# ----------------------------------------------------------------------
# 4. For a given user, infer home city and build city list with costs
# ----------------------------------------------------------------------
def get_home_city(user_code):
    """Most frequent departure city for this user."""
    user_df = df[df['userCode'] == user_code]
    if user_df.empty:
        return None
    return user_df['from'].mode()[0]

def prepare_cities_for_user(user_code):
    home = get_home_city(user_code)
    if home is None:
        raise ValueError(f"User {user_code} not found in data.")
    destinations = [c for c in cities if c != home]
    city_data = []
    for dest in destinations:
        cost = get_round_trip_cost(home, dest)
        value = attraction[dest]
        city_data.append({'city': dest, 'cost': round(cost, 2), 'value': value})
    return home, city_data

# ----------------------------------------------------------------------
# 5. Dynamic Programming (knapsack with cardinality constraint)
# ----------------------------------------------------------------------
def knapsack_with_count(city_data, budget, N):
    """
    city_data: list of dicts with 'cost', 'value'
    budget: maximum total cost
    N: number of cities to select (if possible)
    Returns: (max_value, selected_indices)
    """
    n = len(city_data)
    # Convert budget to integer cents to avoid float issues
    scale = 100
    max_budget = int(budget * scale)
    costs = [int(round(cd['cost'] * scale)) for cd in city_data]
    values = [cd['value'] for cd in city_data]

    # dp[item][budget_cents][k] = max value
    # We'll use a 2D DP: dp[w][k] = max value using items up to current, then iterate items.
    dp = [[-1] * (N + 1) for _ in range(max_budget + 1)]
    dp[0][0] = 0  # zero cost, zero items -> 0 value

    # For backtracking
    choice = [[[False] * (N + 1) for _ in range(max_budget + 1)] for __ in range(n)]

    for i in range(n):
        cost_i = costs[i]
        val_i = values[i]
        # traverse backwards to avoid reusing same item
        for w in range(max_budget, cost_i - 1, -1):
            for k in range(N, 0, -1):
                if dp[w - cost_i][k - 1] != -1:
                    new_val = dp[w - cost_i][k - 1] + val_i
                    if new_val > dp[w][k]:
                        dp[w][k] = new_val
                        choice[i][w][k] = True

    # Find the best budget usage that achieves at least some value; prefer exactly N items if possible.
    best_val = -1
    best_w = 0
    for w in range(max_budget + 1):
        if dp[w][N] > best_val:
            best_val = dp[w][N]
            best_w = w
    if best_val == -1:  # cannot get exactly N, try to get as many as possible up to N
        for k in range(N, 0, -1):
            for w in range(max_budget + 1):
                if dp[w][k] > best_val:
                    best_val = dp[w][k]
                    best_w = w
            if best_val != -1:
                N_used = k
                break
    else:
        N_used = N

    if best_val == -1:
        return 0, []

    # Backtrack to find selected items
    selected = []
    w = best_w
    k = N_used
    for i in range(n - 1, -1, -1):
        if choice[i][w][k]:
            selected.append(i)
            w -= costs[i]
            k -= 1
    selected.reverse()
    return best_val, selected

# ----------------------------------------------------------------------
# 6. Main recommendation function
# ----------------------------------------------------------------------
def recommend_cities(user_code, budget, num_cities):
    home, city_data = prepare_cities_for_user(user_code)
    max_value, indices = knapsack_with_count(city_data, budget, num_cities)
    recommended = [city_data[i]['city'] for i in indices]
    total_cost = sum(city_data[i]['cost'] for i in indices)
    total_value = sum(city_data[i]['value'] for i in indices)
    print(f"\nUser {user_code} | Home: {home}")
    print(f"Budget: {budget:.2f} | Requested cities: {num_cities}")
    print(f"Recommended cities ({len(recommended)}): {recommended}")
    print(f"Total cost: {total_cost:.2f} | Total attraction value: {total_value}")
    for i in indices:
        c = city_data[i]
        print(f"  {c['city']}: cost {c['cost']:.2f}, value {c['value']}")
    return recommended

# ----------------------------------------------------------------------
# 7. Sample test cases
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Test with a few users and budgets
    # User 2 (most frequent home?)
    print("=== Test 1: User 2, budget 5000, cities 3 ===")
    recommend_cities(2, 5000, 3)

    print("\n=== Test 2: User 10, budget 3000, cities 4 ===")
    recommend_cities(10, 3000, 4)

    print("\n=== Test 3: User 0, budget 2000, cities 2 ===")
    recommend_cities(0, 2000, 2)

    # Try a user not in data
    print("\n=== Test 4: User 999 (non‑existent) ===")
    try:
        recommend_cities(999, 5000, 3)
    except ValueError as e:
        print("Error:", e)

import argparse
import csv

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--team-map', required=True, help='Path to team map CSV file')
parser.add_argument('-p', '--product-master', required=True, help='Path to product master CSV file')
parser.add_argument('-s', '--sales', required=True, help='Path to sales CSV file')
parser.add_argument('--team-report', required=True, help='Path to team report CSV file')
parser.add_argument('--product-report', required=True, help='Path to product report CSV file')
args = parser.parse_args()

# Read team map CSV file and store data in a dictionary
team_map = {}
with open(args.team_map, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        team_map[int(row['TeamID'])] = row['Name']

# Read product master CSV file and store data in a dictionary
product_master = {}
with open(args.product_master, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        product_master[int(row[1])] = {'Name': row[2], 'Price': float(row[3]), 'LotSize': int(row[4])}

# Calculate total gross revenue for each team and product from sales data
team_revenue = {}
product_revenue = {}
product_discount = {}
with open(args.sales, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        product_id = int(row[1])
        team_id = int(row[2])
        quantity = int(row[3])
        price = product_master[product_id]['Price'] * product_master[product_id]['LotSize']  # Calculate price per lot
        revenue = price * quantity
        discount = float(row[4]) / 100 * revenue
        team_revenue[team_id] = team_revenue.get(team_id, 0) + revenue
        product_revenue[product_id] = product_revenue.get(product_id, 0) + revenue
        product_discount[product_id] = product_discount.get(product_id, 0) + discount

# Sort team and product data by gross revenue
team_sorted = sorted(team_revenue.items(), key=lambda x: x[1], reverse=True)
product_sorted = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)

# Write team report to CSV file
with open(args.team_report, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Team', 'GrossRevenue'])
    for team_id, revenue in team_sorted:
        writer.writerow([team_map[team_id], revenue])

# Write product report to CSV file
with open(args.product_report, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'GrossRevenue', 'TotalUnits', 'DiscountCost'])
    for product_id, revenue in product_sorted:
        name = product_master[product_id]['Name']
        total_units = product_revenue[product_id] / (product_master[product_id]['Price'] * product_master[product_id]['LotSize'])
        discount_cost = product_discount[product_id]
        writer.writerow([name, revenue, total_units, discount_cost])

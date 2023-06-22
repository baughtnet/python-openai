AI says: Sure, here's a program that reads a CSV file, calculates and displays some statistics:

```
import csv

filename = "data.csv"

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)

    num_rows = 0
    total_sales = 0
    max_sales = 0
    min_sales = float('inf')

    for row in csvreader:
        num_rows += 1
        sales = float(row[1])
        total_sales += sales

        if sales > max_sales:
            max_sales = sales

        if sales < min_sales:
            min_sales = sales

    avg_sales = total_sales / num_rows

    print("Total sales: $", total_sales)
    print("Average sales: $", avg_sales)
    print("Maximal sales: $", max_sales)
    print("Minimal sales: $", min_sales)
```

This program reads a file named `data.csv` that contains rows with two values: a name and a sales amount. It calculates the total, average, maximum, and minimum sales values and prints them.
---------------------------------------

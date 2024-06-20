import pandas as pd
import matplotlib.pyplot as plt
import os
# Suppress warnings
import warnings
warnings.filterwarnings("ignore")

def calculate_one_time_run_production_plan(total_production, setup_cost_per_run, holding_cost_per_item_per_period, period_demand, output_directory, period_label=""):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialise lists to store results
    num_periods = len(period_demand)
    production = [0] * num_periods
    production[0] = total_production  # All production happens in the first period
    ioh = [0] * num_periods
    holding_cost = [0] * num_periods
    setup_cost = [0] * num_periods
    total_cost = [0] * num_periods

    # Calculating Inventory on Hand (IOH) and costs
    ioh[0] = total_production - period_demand[0]
    holding_cost[0] = ioh[0] * holding_cost_per_item_per_period
    setup_cost[0] = setup_cost_per_run
    total_cost[0] = holding_cost[0] + setup_cost[0]

    for period in range(1, num_periods):
        ioh[period] = ioh[period - 1] - period_demand[period]
        holding_cost[period] = ioh[period] * holding_cost_per_item_per_period
        setup_cost[period] = 0  # No setup cost after the first period
        total_cost[period] = holding_cost[period]

    # Creating a DataFrame to display the results
    data = {
        period_label: list(range(1, num_periods + 1)),
        "Forecast": period_demand,
        "Production": production,
        "IOH": ioh,
        "Holding Cost": holding_cost,
        "Set-Up Costs": setup_cost,
        "Total Cost": total_cost,
    }

    df = pd.DataFrame(data)
    df["Total Cost"] = df["Holding Cost"] + df["Set-Up Costs"]

    # Calculate totals
    total_row = pd.DataFrame({
        period_label: ["Total"],
        "Forecast": [sum(period_demand)],
        "Production": [sum(production)],
        "IOH": [sum(ioh)],
        "Holding Cost": [sum(holding_cost)],
        "Set-Up Costs": [sum(setup_cost)],
        "Total Cost": [sum(total_cost)],
    })

    # Concatenate the total row to the DataFrame
    df = pd.concat([df, total_row], ignore_index=True)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(df[period_label][:-1], df['Forecast'][:-1], 'bo-', label='Forecast')  # Blue diamonds
    plt.plot(df[period_label][:-1], df['Production'][:-1], 'rs-', label='Production')  # Red squares
    plt.plot(df[period_label][:-1], df['IOH'][:-1], 'g^-', label='IOH')  # Green triangles
    plt.xlabel(period_label)
    plt.ylabel('Units')
    plt.title(f'One Time Run Production Plan ({period_label})')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plot_path = os.path.join(output_directory, "one_time_run_plot.png")
    plt.savefig(plot_path)
    plt.show()

    # Save DataFrame
    df_path = os.path.join(output_directory, "one_time_run_production_plan.csv")
    df.to_csv(df_path, index=False)

    return df, plot_path, df_path
# ____________________________________________________________________________

def calculate_lot_for_lot_production_plan(setup_cost_per_run, holding_cost_per_item_per_period, period_demand, output_directory, period_label=""):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialise lists to store results
    num_periods = len(period_demand)
    production = period_demand.copy()  # Production equals demand for each period
    ioh = [0] * num_periods
    holding_cost = [0] * num_periods
    setup_cost = [setup_cost_per_run] * num_periods
    total_cost = [0] * num_periods

    # Calculate costs for each period
    for period in range(num_periods):
        holding_cost[period] = ioh[period] * holding_cost_per_item_per_period
        total_cost[period] = holding_cost[period] + setup_cost[period]

    # Creating a DataFrame to display the results
    data = {
        period_label: list(range(1, num_periods + 1)),
        "Forecast": period_demand,
        "Production": production,
        "IOH": ioh,
        "Holding Cost": holding_cost,
        "Set-Up Costs": setup_cost,
        "Total Cost": total_cost,
    }

    df = pd.DataFrame(data)
    df["Total Cost"] = df["Holding Cost"] + df["Set-Up Costs"]

    # Calculate totals
    total_row = pd.DataFrame({
        period_label: ["Total"],
        "Forecast": [sum(period_demand)],
        "Production": [sum(production)],
        "IOH": [sum(ioh)],
        "Holding Cost": [sum(holding_cost)],
        "Set-Up Costs": [sum(setup_cost)],
        "Total Cost": [sum(total_cost)],
    })

    # Concatenate the total row to the DataFrame
    df = pd.concat([df, total_row], ignore_index=True)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(df[period_label][:-1], df['Forecast'][:-1], 'bo-', label='Forecast')  # Blue diamonds
    plt.plot(df[period_label][:-1], df['Production'][:-1], 'rs-', label='Production')  # Red squares
    plt.plot(df[period_label][:-1], df['IOH'][:-1], 'g^-', label='IOH')  # Green triangles
    plt.xlabel(period_label)
    plt.ylabel('Units')
    plt.title(f'Lot for Lot Production Plan ({period_label})')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plot_path = os.path.join(output_directory, "lot_for_lot_plot.png")
    plt.savefig(plot_path)
    plt.show()

    # Save DataFrame
    df_path = os.path.join(output_directory, "lot_for_lot_production_plan.csv")
    df.to_csv(df_path, index=False)

    return df, plot_path, df_path

#-------------------------------------------------------------------------------

def calculate_fixed_order_quantity_production_plan(fixed_order_quantity, setup_cost_per_run, holding_cost_per_item_per_period, period_demand, output_directory, period_label="Month"):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialise lists to store results
    num_periods = len(period_demand)
    production = [0] * num_periods
    ioh = [0] * num_periods
    holding_cost = [0] * num_periods
    setup_cost = [0] * num_periods
    total_cost = [0] * num_periods

    # Calculating Inventory on Hand (IOH) and costs
    for period in range(num_periods):
        if period == 0:
            production[period] = fixed_order_quantity
            ioh[period] = production[period] - period_demand[period]
            setup_cost[period] = setup_cost_per_run
        else:
            if period_demand[period] > ioh[period - 1]:
                production[period] = fixed_order_quantity
                setup_cost[period] = setup_cost_per_run
                ioh[period] = ioh[period - 1] + production[period] - period_demand[period]
            else:
                production[period] = 0
                setup_cost[period] = 0
                ioh[period] = ioh[period - 1] - period_demand[period]

        ioh[period] = max(ioh[period], 0)
        holding_cost[period] = ioh[period] * holding_cost_per_item_per_period
        total_cost[period] = holding_cost[period] + setup_cost[period]

    # Creating a DataFrame to display the results
    data = {
        period_label: list(range(1, num_periods + 1)),
        "Forecast": period_demand,
        "Production": production,
        "IOH": ioh,
        "Holding Cost": holding_cost,
        "Set-Up Costs": setup_cost,
        "Total Cost": total_cost,
    }

    df = pd.DataFrame(data)
    df["Total Cost"] = df["Holding Cost"] + df["Set-Up Costs"]

    # Calculate totals
    total_row = pd.DataFrame({
        period_label: ["Total"],
        "Forecast": [sum(period_demand)],
        "Production": [sum(production)],
        "IOH": [sum(ioh)],
        "Holding Cost": [sum(holding_cost)],
        "Set-Up Costs": [sum(setup_cost)],
        "Total Cost": [sum(total_cost)],
    })

    # Concatenate the total row to the DataFrame
    df = pd.concat([df, total_row], ignore_index=True)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(df[period_label][:-1], df['Forecast'][:-1], 'bo-', label='Forecast')  # Blue diamonds
    plt.plot(df[period_label][:-1], df['Production'][:-1], 'rs-', label='Production')  # Red squares
    plt.plot(df[period_label][:-1], df['IOH'][:-1], 'g^-', label='IOH')  # Green triangles
    plt.xlabel(period_label)
    plt.ylabel('Units')
    plt.title(f'Fixed Order Quantity Production Plan ({period_label})')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plot_path = os.path.join(output_directory, "fixed_order_quantity_plot.png")
    plt.savefig(plot_path)
    plt.show()

    # Save DataFrame
    df_path = os.path.join(output_directory, "fixed_order_quantity_production_plan.csv")
    df.to_csv(df_path, index=False)

    return df, plot_path, df_path

#--------------------------------------------------------------------

def calculate_periodic_order_quantity_production_plan(order_period, setup_cost_per_run, holding_cost_per_item_per_period, period_demand, output_directory, period_label=""):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Initialise lists to store results
    num_periods = len(period_demand)
    production = [0] * num_periods
    ioh = [0] * num_periods
    holding_cost = [0] * num_periods
    setup_cost = [0] * num_periods
    total_cost = [0] * num_periods

    # Calculating Inventory on Hand (IOH) and costs
    for period in range(num_periods):
        if period % order_period == 0:
            order_quantity = sum(period_demand[period:period + order_period])
            production[period] = order_quantity
            setup_cost[period] = setup_cost_per_run
        else:
            production[period] = 0
            setup_cost[period] = 0

        if period == 0:
            ioh[period] = production[period] - period_demand[period]
        else:
            ioh[period] = ioh[period - 1] + production[period] - period_demand[period]

        holding_cost[period] = ioh[period] * holding_cost_per_item_per_period
        total_cost[period] = holding_cost[period] + setup_cost[period]

    # Creating a DataFrame to display the results
    data = {
        period_label: list(range(1, num_periods + 1)),
        "Forecast": period_demand,
        "Production": production,
        "IOH": ioh,
        "Holding Cost": holding_cost,
        "Set-Up Costs": setup_cost,
        "Total Cost": total_cost,
    }

    df = pd.DataFrame(data)
    df["Total Cost"] = df["Holding Cost"] + df["Set-Up Costs"]

    # Calculate totals
    total_row = pd.DataFrame({
        period_label: ["Total"],
        "Forecast": [sum(period_demand)],
        "Production": [sum(production)],
        "IOH": [sum(ioh)],
        "Holding Cost": [sum(holding_cost)],
        "Set-Up Costs": [sum(setup_cost)],
        "Total Cost": [sum(total_cost)],
    })

    # Concatenate the total row to the DataFrame
    df = pd.concat([df, total_row], ignore_index=True)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(df[period_label][:-1], df['Forecast'][:-1], 'bo-', label='Forecast')  # Blue diamonds
    plt.plot(df[period_label][:-1], df['Production'][:-1], 'rs-', label='Production')  # Red squares
    plt.plot(df[period_label][:-1], df['IOH'][:-1], 'g^-', label='IOH')  # Green triangles
    plt.xlabel(period_label)
    plt.ylabel('Units')
    plt.title(f'Periodic Order Quantity Production Plan ({period_label})')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plot_path = os.path.join(output_directory, "periodic_order_quantity_plot.png")
    plt.savefig(plot_path)
    plt.show()

    # Save DataFrame
    df_path = os.path.join(output_directory, "periodic_order_quantity_production_plan.csv")
    df.to_csv(df_path, index=False)

    return df, plot_path, df_path

#------------------------------------------------------------------------------

def calculate_and_compare_metrics(demand_data, dfs, approaches):
    def calculate_comparison_metrics(df, total_demand):
        # Exclude the total row for inventory calculations
        df = df.iloc[:-1]
        # Calculate total inventory on hand
        total_inventory = df['IOH'].sum()
        # Calculate average inventory on hand
        avg_inventory_on_hand = round(total_inventory / len(df.index), 1)
        # Calculate inventory turns
        inventory_turns = round((total_demand / avg_inventory_on_hand), 1)

        inventory_cost = df['Holding Cost'].sum()
        setup_cost = df['Set-Up Costs'].sum()
        total_cost = df['Total Cost'].sum()

        return inventory_cost, setup_cost, total_cost, avg_inventory_on_hand, inventory_turns

    # Total demand for the period
    total_demand = sum(demand_data)

    # Calculate metrics for each heuristic approach
    metrics = [calculate_comparison_metrics(df, total_demand) for df in dfs]

    # Create the summary table
    comparison_data = {
        'Approach': approaches,
        'Inventory Costs': [metric[0] for metric in metrics],
        'Set-Up Costs': [metric[1] for metric in metrics],
        'Total Costs': [metric[2] for metric in metrics],
        'Avg Monthly IOH': [metric[3] for metric in metrics],
        'Inventory Turns': [metric[4] for metric in metrics],
    }

    comparison_df = pd.DataFrame(comparison_data)

    return comparison_df


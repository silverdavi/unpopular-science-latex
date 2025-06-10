import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# Define the functions
def v1(x, M, R):
    """Blue curve: v = M * (1 - exp(-x/R))"""
    return M * (1 - np.exp(-x / R))

def v2(x, A=12400, k=1.113, t=-9200, L=16.4):
    """Gray curve: hardcoded parameters"""
    numerator = A * (x**k + t)
    denominator = (x**k + t + A)**1.5
    return numerator / denominator + L

# Function to read the CSV data
def read_data():
    try:
        # Try to read the CSV file
        df = pd.read_csv('m33_rotation.csv')
        # Convert kpc to pc (assuming data is in kpc)
        df['radius_pc'] = df['radius'] * 1000
        return df
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

# Main plotting function
def plot_rotation_curve():
    # Read the data
    df = read_data()
    
    if df is None:
        print("Cannot proceed without data")
        return
    
    # Extract data for fitting
    x_data = df['radius_pc'].values
    y_data = df['velocity'].values
    y_err = df['velocity_error'].values
    
    # Fit v1 to the data
    initial_guess = [117, 8040]  # M, R
    bounds = ([80, 1000], [150, 15000])
    
    try:
        params, covariance = curve_fit(v1, x_data, y_data, p0=initial_guess, 
                                       sigma=y_err, bounds=bounds)
        M_fit, R_fit = params
    except RuntimeError as e:
        print(f"Fitting failed: {e}")
        M_fit, R_fit = initial_guess
    
    # Define the x range for the models
    x = np.linspace(1000, 30000, 1000)
    
    # Calculate the y values for both functions
    y1 = v1(x, M_fit, R_fit)  # Use fitted parameters
    y2 = v2(x)  # Use hardcoded parameters
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot the data with explicit label
    data_points = ax.errorbar(x_data, y_data, yerr=y_err, 
                fmt='o', color='gold', 
                capsize=3, markersize=5, ecolor='gold', alpha=0.7)
    data_points.set_label('Observed data')
    
    # Plot the models with explicit labels
    line1, = ax.plot(x, y1, '-', color='blue', linewidth=2.5)
    line1.set_label('Model with dark matter')
    
    line2, = ax.plot(x, y2, '--', color='gray', linewidth=2.5)
    line2.set_label('Model without dark matter')
    
    # Set plot properties
    ax.set_xlabel('Radius (pc)', fontsize=14)
    ax.set_ylabel('Rotation Velocity (km/s)', fontsize=14)
    ax.set_title('M33 Galaxy Rotation Curve', fontsize=16)
    ax.set_xlim(0, 30000)
    ax.set_ylim(0, 140)
    
    # Create a second x-axis on top showing kpc for reference
    ax2 = ax.twiny()
    ax2.set_xlim(0, 30)  # Same range but in kpc
    ax2.set_xlabel('Radius (kpc)', fontsize=14)
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('m33_rotation_curve.png', dpi=300)
    plt.show()

# Run the main function
if __name__ == "__main__":
    plot_rotation_curve()
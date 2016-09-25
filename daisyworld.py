from daisy_growth_rate import daisy_growth_rate
import numpy
import matplotlib.pyplot as pyplot
#% matplotlib inline


#Daisyworld model
def Daisyworld(Total_Time):

    # Arguments

    # Constant variables
    albedo_daisies = 0.85   # albedo of daisies, unitless
    albedo_soil = 0.15      # albedo of soil, unitless
    Initial_Daisies = 0.5   # initial fractional coverage of daisies
    S = 917                 # solar energy, in W/m2
    sigma = 5.67e-8         # Stefan-Boltzmann constant, in W/m2/K4
    death_rate = 0.3        # rate of daisy death

    # Use spacing based on elapsed_time
    time = numpy.arange(0,Total_Time,1)

    # Define an array of zeros to store the output variables
    area_daisies = numpy.zeros(len(time))  # fractional coverage of daisies
    T = numpy.zeros(len(time))             # surface temperature

    # Set the initial conditions
    area_daisies[0] = Initial_Daisies

    # Calculate the original albedo based on the initial condition for daisies
    albedo = area_daisies[0] * albedo_daisies + (1-area_daisies[0]) * albedo_soil

    # Calculate the original temperature based on the original albedo
    T[0] = ((S*(1-albedo))/sigma)**0.25

    # Loop over time steps - each time calculate albedo, growth rate, temperature, area_change and area
    for i in range(1,len(time)):

        # Define growth_rate using equation
        growth_rate = 1 - 0.003265*(295.5-T[i-1])**2

        # Avoid negative values
        if growth_rate < 0:
            growth_rate = 0

        # Calculate change in area - based on the area from the previous time step
        area_change = area_daisies[i-1] * ((1-area_daisies[i-1]) * growth_rate - death_rate)

        # Finally, add the area change (which can be positve or negative) to the prior area
        area_daisies[i] = area_daisies[i-1] + area_change

        # Define the planetary albedo based on the new coverage of daisies just calculated
        albedo = area_daisies[i] * albedo_daisies + (1-area_daisies[i]) * albedo_soil

        # Calculate the temperature using the albedo calculated above
        T[i] = ((S*(1-albedo))/sigma)**0.25

    return time,area_daisies,T

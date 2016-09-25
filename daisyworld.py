from daisy_growth_rate import daisy_growth_rate
import numpy
import matplotlib.pyplot as pyplot
#% matplotlib inline


#Daisyworld model
def Daisyworld(Total_Time):

    # Constants
    S = 917                 # solar energy, in W/m2
    sigma = 5.67e-8         # Stefan-Boltzmann constant, in W/m2/K4


    # Black Daisy paramters
    blackDaisy_albedio = 0.15 # albedo of black daisies, unitless
    blackDaisy_inital_coverage = 0.25 #initial fractional coverage of black daisies

    # White Daisy paramters
    whiteDaisy_albedio = 0.85 # albedo of black daisies, unitless
    whiteDaisy_inital_coverage = 0.25 #initial fractional coverage of black daisies


    # Planet parameters
    albedo_soil = 0.15      # albedo of soil, unitless


    # Use spacing based on elapsed_time
    time = numpy.arange(0,Total_Time,1)


    # Define an array of zeros to store the output variables
    blackDaisy_coverage = numpy.zeros(len(time)) # fractional coverage of Black daisies
    whiteDaisy_coverage = numpy.zeros(len(time)) # fractional coverage of White daisies
    T = numpy.zeros(len(time)) # surface temperature


########################## continue from here











    # Set the initial conditions
    area_daisies[0] = Initial_Daisies

    # Calculate the original albedo based on the initial condition for daisies
    albedo = area_daisies[0] * albedo_daisies + (1-area_daisies[0]) * albedo_soil

    # Calculate the original temperature based on the original albedo
    T[0] = ((S*(1-albedo))/sigma)**0.25

    # Loop over time steps - each time calculate albedo, growth rate, temperature, area_change and area
    for i in range(1,len(time)):

        # Define growth_rate using equation
        #old equation: growth_rate = 1 - 0.003265*(295.5-T[i-1])**2

        # New equation incorperates death_rate at either end of temperature scale
        growth_rate = daisy_growth_rate(288, 318, T[i-1])
        print growth_rate


        # Calculate change in area - based on the area from the previous time step
        # old: area_change = area_daisies[i-1] * ((1-area_daisies[i-1]) * growth_rate - death_rate)

        #new: removed death_rate as it is incorperated in growth_rate


        # Finally, add the area change (which can be positve or negative) to the prior area
        area_daisies[i] = area_daisies[i-1] + area_change

        # Define the planetary albedo based on the new coverage of daisies just calculated
        albedo = area_daisies[i] * albedo_daisies + (1-area_daisies[i]) * albedo_soil

        # Calculate the temperature using the albedo calculated above
        T[i] = ((S*(1-albedo))/sigma)**0.25

    return time,area_daisies,T
print Daisyworld(100)

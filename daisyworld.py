from daisy_growth_rate import daisy_growth_rate
from avg_albedo import *
from conversions import *
import numpy
import matplotlib.pyplot as pyplot
#% matplotlib inline


#Daisyworld model
def Daisyworld(Total_Time):

    # Constants
    S = 917                 # solar energy, in W/m2
    sigma = 5.67e-8         # Stefan-Boltzmann constant, in W/m2/K4


    # Black Daisy paramters
    blackDaisy_albedio = 0.05 # albedo of black daisies, unitless
    blackDaisy_inital_coverage = 0.15 #initial fractional coverage of black daisies

    # White Daisy paramters
    whiteDaisy_albedio = 0.8 # albedo of black daisies, unitless
    whiteDaisy_inital_coverage = 0.6 #initial fractional coverage of black daisies


    # Planet parameters
    albedo_soil = 0.15      # albedo of soil, unitless


    # Use spacing based on elapsed_time
    time = numpy.arange(0,Total_Time,1)


    # Define an array of zeros to store the output variables
    blackDaisy_coverage = numpy.zeros(len(time)) # fractional coverage of Black daisies
    whiteDaisy_coverage = numpy.zeros(len(time)) # fractional coverage of White daisies
    T = numpy.zeros(len(time)) # surface temperature
    area_daisies = numpy.zeros(len(time)) #fractional coverage of Black and White daisies
    area_soil = numpy.zeros(len(time)) #fractional coverage of soil
    avg_albedo_daisiesArray = numpy.zeros(len(time)) #Array of average albedo of Black and White daisies combined

    # Set the initial conditions
    area_daisies[0] = blackDaisy_inital_coverage + whiteDaisy_inital_coverage
    area_soil[0] = 1 - area_daisies[0]
    whiteDaisy_coverage[0] = whiteDaisy_inital_coverage
    blackDaisy_coverage[0] = blackDaisy_inital_coverage


    # check the area of daisies is not above 100%
    if area_daisies[0] > 1:
        print "blackDaisy_inital_coverage + whiteDaisy_inital_coverage was larger than 1"
        exit()

    # Calculate the original albedo based on the initial condition for daisies
    #old: albedo = area_daisies[0] * albedo_daisies + (1-area_daisies[0]) * albedo_soil
    albedo = avg_albedo(blackDaisy_inital_coverage, blackDaisy_albedio, whiteDaisy_inital_coverage, whiteDaisy_albedio, area_soil[0], albedo_soil)

    # Calculate the original temperature based on the original albedo
    T[0] = ((S*(1-albedo))/sigma)**0.25
    print "initial temp:" + str(k_to_c(T[0]))

    # Loop over time steps - each time calculate albedo, growth rate, temperature, area_change and area
    for i in range(1,len(time)):

        # Define growth_rate using equation
        #old equation: growth_rate = 1 - 0.003265*(295.5-T[i-1])**2

        # New equation incorperates death_rate at either end of temperature scale
        whiteDaisy_growth_rate = daisy_growth_rate(c_to_k(15), c_to_k(45), T[i-1])
        blackDaisy_growth_rate = daisy_growth_rate(c_to_k(-5), c_to_k(25), T[i-1])
        print "whiteDaisy_growth_rate:" + str(whiteDaisy_growth_rate)
        print "blackDaisy_growth_rate:" + str(blackDaisy_growth_rate)


        # Calculate change in area - based on the area from the previous time step
        # old: area_change = area_daisies[i-1] * ((1-area_daisies[i-1]) * growth_rate - death_rate)
        #removed death_rate as it is incorperated in growth_rate
        ############ THIS IS UNINHIBITED AREA CHANGE
        whiteDaisy_area_change = whiteDaisy_coverage[i-1] * whiteDaisy_growth_rate
        blackDaisy_area_change = blackDaisy_coverage[i-1] * blackDaisy_growth_rate
        print "whiteDaisy_area_change: " + str(whiteDaisy_area_change)
        print "blackDaisy_area_change: " + str(blackDaisy_area_change)
        print "area_daisies[i-1]:" + str(area_daisies[i-1])

        ############# CONSTRIAINING FACTORS
        ###########

        ##### Check if the daisy growth exceeds the available soil area - IS THIS NEEDED AS THEY ARE GROWTH RATES!!!
        if (whiteDaisy_area_change + blackDaisy_area_change > 1):
            print "Need to Limit to available area (Cross that bridge when we get to it)"
            ##### Limit Daisy Growth to fill available area
            ##### Ratio of growth rates?

        ##### Increase the daisy area and daisy coverage by the required value




######################continue













        # Finally, add the area change (which can be positve or negative) to the prior area
        area_daisies[i] = area_daisies[i-1] + area_change

        # Define the planetary albedo based on the new coverage of daisies just calculated
        albedo = area_daisies[i] * albedo_daisies + (1-area_daisies[i]) * albedo_soil

        # Calculate the temperature using the albedo calculated above
        T[i] = ((S*(1-albedo))/sigma)**0.25

    return time,area_daisies,T
print Daisyworld(100)

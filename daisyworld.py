from daisy_growth_rate import daisy_growth_rate
from avg_albedo import *
from conversions import *
import numpy
import matplotlib.pyplot as pyplot
#% matplotlib inline


#Daisyworld model
def Daisyworld(Total_Time):

    # Constants
    S = 500                 # solar energy, in W/m2
    sigma = 5.67e-8         # Stefan-Boltzmann constant, in W/m2/K4


    # Black Daisy paramters
    blackDaisy_albedio = 0.05 # albedo of black daisies, unitless
    blackDaisy_inital_coverage = 0.05 #initial fractional coverage of black daisies
    blackDaisy_minimumTemp = c_to_k(-5) # minimum temperature daisy will survive
    blackDaisy_maximumTemp = c_to_k(25) # minimum temperature daisy will survive

    # White Daisy paramters
    whiteDaisy_albedio = 0.8 # albedo of black daisies, unitless
    whiteDaisy_inital_coverage = 0.1 #initial fractional coverage of black daisies
    whiteDaisy_minimumTemp = c_to_k(5) # minimum temperature daisy will survive
    whiteDaisy_maximumTemp = c_to_k(45) # maximum temperature daisy will survive

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


    # Loop over time steps - each time calculate albedo, growth rate, temperature, area_change and area
    for i in range(1,len(time)):






        # Define growth_rate using equation
        #old equation: growth_rate = 1 - 0.003265*(295.5-T[i-1])**2

        # New equation incorperates death_rate at either end of temperature scale
        whiteDaisy_growth_rate = daisy_growth_rate(whiteDaisy_minimumTemp, whiteDaisy_maximumTemp, T[i-1])
        blackDaisy_growth_rate = daisy_growth_rate(blackDaisy_minimumTemp, blackDaisy_maximumTemp, T[i-1])



        #### work out if growth rates need scaling - so the daisies can share the available space.
        if (whiteDaisy_growth_rate + blackDaisy_growth_rate > 1): # i.e. if the daisies each want to grow more than the available area, scale their growth rate based on the ratio
            scale_factor = 1 / (whiteDaisy_growth_rate + blackDaisy_growth_rate)
            whiteDaisy_growth_rate = whiteDaisy_growth_rate * scale_factor
            blackDaisy_growth_rate = blackDaisy_growth_rate * scale_factor


        ### Work out new daisy coverage
        whiteDaisy_coverage[i] = whiteDaisy_coverage[i-1] + (whiteDaisy_coverage[i-1] * whiteDaisy_growth_rate)
        blackDaisy_coverage[i] = blackDaisy_coverage[i-1] + (blackDaisy_coverage[i-1] * blackDaisy_growth_rate)


        ### Update Output variables
        area_daisies[i] = blackDaisy_coverage[i] + whiteDaisy_coverage[i]
        area_soil[i] = 1 - area_daisies[i]
        albedo = avg_albedo(blackDaisy_inital_coverage, blackDaisy_albedio, whiteDaisy_inital_coverage, whiteDaisy_albedio, area_soil[i], albedo_soil)
        T[i] = ((S*(1-albedo))/sigma)**0.25


    return time,k_to_c(T),area_daisies,area_soil,whiteDaisy_coverage, blackDaisy_coverage,albedo
a = Daisyworld(100)
pyplot.plot(a[0],a[1])
pyplot.plot(a[0],a[4])
pyplot.plot(a[0],a[5])
pyplot.show()

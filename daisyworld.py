
########################## IMPORTS
from daisy_growth_rate import daisy_growth_rate
from avg_albedo import *
from conversions import *
import numpy
import matplotlib.pyplot as pyplot
#% matplotlib inline
##########################


def Daisyworld(Total_Time, *plots):

    debug = 0


    ########################## Constants
    sigma = 5.67e-8         # Stefan-Boltzmann constant, in W/m2/K4
    ##########################

    # Use spacing based on elapsed_time
    time = numpy.arange(0,Total_Time,1)



    ########################## Daisy paramters

    # Common
    area_daisies = numpy.zeros(len(time)) #fractional coverage of Black and White daisies
    avg_albedo_daisiesArray = numpy.zeros(len(time)) #Array of average albedo of Black and White daisies combined

    # Black Daisy paramters
    blackDaisy_albedio = 0.05 # albedo of black daisies, unitless
    blackDaisy_inital_coverage = 0.05 #initial fractional coverage of black daisies
    blackDaisy_minimumTemp = c_to_k(-5) # minimum temperature daisy will survive
    blackDaisy_maximumTemp = c_to_k(25) # minimum temperature daisy will survive
    blackDaisy_coverage = numpy.zeros(len(time)) # fractional coverage of Black daisies
    ############################################################################################ insert blackDaisy_ = numpy.zeros(len(time)) # fractional coverage of Black daisies

    # White Daisy paramters
    whiteDaisy_albedio = 0.8 # albedo of black daisies, unitless
    whiteDaisy_inital_coverage = 0.1 #initial fractional coverage of black daisies
    whiteDaisy_minimumTemp = c_to_k(5) # minimum temperature daisy will survive
    whiteDaisy_maximumTemp = c_to_k(45) # maximum temperature daisy will survive
    whiteDaisy_coverage = numpy.zeros(len(time)) # fractional coverage of White daisies
    ############################################################################################ insert blackDaisy_ = numpy.zeros(len(time)) # fractional coverage of Black daisies
    ##########################




    ########################## Planet parameters
    S = 700                 # solar energy, in W/m2
    albedo_soil = 0.15      # albedo of soil, unitless
    area_soil = numpy.zeros(len(time)) #fractional coverage of soil
    T = numpy.zeros(len(time)) # surface temperature
    albedo = numpy.zeros(len(time)) # planet albedo
    ##########################










    ########################## Set the initial conditions
    area_daisies[0] = blackDaisy_inital_coverage + whiteDaisy_inital_coverage
    if debug: print "area_daisies[0]" + str(area_daisies[0])
    area_soil[0] = 1 - area_daisies[0]
    if debug: print "area_soil[0]" + str(area_soil[0])
    whiteDaisy_coverage[0] = whiteDaisy_inital_coverage
    if debug: print "whiteDaisy_coverage[0]" + str(whiteDaisy_coverage[0])
    blackDaisy_coverage[0] = blackDaisy_inital_coverage
    if debug: print "blackDaisy_coverage[0]" + str(blackDaisy_coverage[0])

    # check the area of daisies is not above 100%
    if area_daisies[0] > 1:
        if debug: print "blackDaisy_inital_coverage + whiteDaisy_inital_coverage was larger than 1"
        exit()

    # Calculate the original albedo based on the initial condition for daisies
    #old: albedo = area_daisies[0] * albedo_daisies + (1-area_daisies[0]) * albedo_soil
    albedo[0] = avg_albedo(blackDaisy_inital_coverage, blackDaisy_albedio, whiteDaisy_inital_coverage, whiteDaisy_albedio, area_soil[0], albedo_soil)

    # Calculate the original temperature based on the original albedo
    T[0] = ((S*(1-albedo[0]))/sigma)**0.25


    # Loop over time steps - each time calculate albedo, growth rate, temperature, area_change and area
    for i in range(1,len(time)):

        # Define growth_rate using equation
        #old equation: growth_rate = 1 - 0.003265*(295.5-T[i-1])**2

        ########################## New equation incorperates death_rate at either end of temperature scale
        whiteDaisy_growth_rate = daisy_growth_rate(whiteDaisy_minimumTemp, whiteDaisy_maximumTemp, T[i-1])
        blackDaisy_growth_rate = daisy_growth_rate(blackDaisy_minimumTemp, blackDaisy_maximumTemp, T[i-1])
        ##########################



        ########################## work out if uninhibited growth rate will exceed the available area.
        whiteDaisy_coverage_test = whiteDaisy_coverage[i-1] + (whiteDaisy_coverage[i-1] * whiteDaisy_growth_rate)
        blackDaisy_coverage_test = blackDaisy_coverage[i-1] + (blackDaisy_coverage[i-1] * blackDaisy_growth_rate)

        total_daisy_coverage_test = whiteDaisy_coverage_test + blackDaisy_coverage_test

        if (total_daisy_coverage_test > area_soil[i-1]):
            ### the daisies will outgrow the available area_soil
            ### Scale the growth to fit
            if debug: print "daisy exceeds soil - scaling"
            scale_factor = 1 / (total_daisy_coverage_test / area_soil[i-1])

            ### new growth rates
            whiteDaisy_growth_rate = whiteDaisy_growth_rate * scale_factor
            blackDaisy_growth_rate = blackDaisy_growth_rate * scale_factor

        ##########################




        ########################## Work out new daisy coverage
        # Debug info
        if debug: print "whiteDaisy_growth_rate "  + str(whiteDaisy_growth_rate)
        if debug: print "blackDaisy_growth_rate " + str(blackDaisy_growth_rate)

        # white daisies
        whiteDaisy_coverage[i] = whiteDaisy_coverage[i-1] + (whiteDaisy_coverage[i-1] * whiteDaisy_growth_rate)
        if whiteDaisy_coverage[i] > 1:
            whiteDaisy_coverage[i] = 1
        if debug: print "new whiteDaisy_coverage " + str(whiteDaisy_coverage[i])

        #black daisies
        blackDaisy_coverage[i] = blackDaisy_coverage[i-1] + (blackDaisy_coverage[i-1] * blackDaisy_growth_rate)
        if blackDaisy_coverage[i] > 1:
            blackDaisy_coverage[i] = 1
        if debug: print "new blackDaisy_coverage " + str(blackDaisy_coverage[i])
        ##########################



        ########################## Update Output variables
        area_daisies[i] = blackDaisy_coverage[i] + whiteDaisy_coverage[i]
        area_soil[i] = 1 - area_daisies[i]
        albedo[i] = avg_albedo(blackDaisy_coverage[i], blackDaisy_albedio, whiteDaisy_coverage[i], whiteDaisy_albedio, area_soil[i], albedo_soil)
        T[i] = ((S*(1-albedo[i-1]))/sigma)**0.25
        ##########################


    if (1 in plots): pyplot.plot(time,k_to_c(T),label="Temp: DegC")
    if (2 in plots): pyplot.plot(time,area_daisies,label="Total Area Daisies: Fraction")
    if (3 in plots): pyplot.plot(time,area_soil,label="Total Area Soil: Fraction")
    if (4 in plots): pyplot.plot(time,whiteDaisy_coverage,label="White Daisy Coverage: Fraction")
    if (5 in plots): pyplot.plot(time,blackDaisy_coverage,label="Black Daisy Coverage: Fraction")
    if (6 in plots): pyplot.plot(time,albedo,label="Planet Albedo")
    if (7 in plots): pyplot.plot(time,whiteDaisy_growth_rate,label="White Daisy Growth Rate: Fraction") # fix
    if (8 in plots): pyplot.plot(time,blackDaisy_growth_rate,label="Black Daisy Growth Rate: Fraction") # fix

    if plots: pyplot.legend(loc='upper left', frameon=False)
    if plots: pyplot.show()

    return time,k_to_c(T),area_daisies,area_soil,whiteDaisy_coverage, blackDaisy_coverage,albedo, whiteDaisy_growth_rate, blackDaisy_growth_rate
a = Daisyworld(10,1,4,5)

def daisy_growth_rate(lzgp=15, uzgp=45, temp=30):

    #growth rate equation using paramters

    ### Variables
    # lzgp - Lower zero growth rate, degC
    # uzgp - Upper zero growth rate, degC
    # temp - Current Temperature

    # Returns: Growth rate value between -1 and 1

    ##################################
    # Math trasnformations from https://www.desmos.com/calculator/lac2i0bgum
    # The following code calculates the equation of a parabola using 3 points
    # Concept from adapted from: http://www3.geosc.psu.edu/~dmb53/DaveSTELLA/Daisyworld/daisyworld_model.htm
    ##################################

    x1 = lzgp
    y1 = 0

    x3 = uzgp
    y3 = 0

    x2 = (x1 + x3)/2
    y2 = 1

    A1 = -(x1**2) + (x2**2)

    B1 = -x1 + x2

    D1 = -y1 + y2

    A2 = -x2**2 + x3**2

    B2 = -x2 + x3

    D2 = -y2 + y3

    Bm = -(B2/B1)

    A3 = Bm * A1 + A2

    D3 = Bm * D1 + D2

    a = D3/float(A3)

    b = (D1 - A1 * a)/B1

    c = y1 - a*x1**2 - b*x1

    growth_rate = a*temp**2 + b*temp + c #adapted from parabola general equation y = ax^2 + bx + c

    if growth_rate < -1:
        growth_rate = -1

    return growth_rate

daisy_growth_rate()

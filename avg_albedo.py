def avg_albedo(coverage1=0, albedo1=0, coverage2=0, albedo2=0, coverage3=0, albedo3=0):
    if (coverage1 > 1) or (coverage2 > 1) or (coverage3 > 1) or (coverage1 + coverage2 + coverage3 > 1):
        print "Coverage cannot be larger than 1"
        print "coverage1:" + str(coverage1)
        print "coverage2:" + str(coverage2)
        print "coverage3:" + str(coverage3)
        exit()

    albedo = coverage1 * albedo1 + coverage2 * albedo2 + coverage3 * albedo3
    return albedo

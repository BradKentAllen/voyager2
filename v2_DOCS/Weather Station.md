# Weather Station



### RH

```
Td = T - ((100-RH)/5)

Td: Dew Point in deg C
T: Temp in deg C
RH: %
```



### Instruments

from Pontis Weather Station

```
#### WEATHER STATION PARAMETERS ####
# radius of the anemometer vanes in centimeters
anemometerRadius = 5.7

# rain gage factor (measured at .04 cm/tip, .4 millimeters of rain per tip)
rainGageVolume = .4
```



### Water loss, Irrigation, Penman-Monteith

```python
#### WATER LOSS and IRRIGATION ####
def penmanMonteith(self, hourTemp, hourRH, hourWindAvr, hourLux, printFactor):
    ''' Calculates mm water lost in 1 hour
    ONLY WORKS FOR 1 HOUR PERIOD
    '''
    if printFactor is True: print(hourTemp, 'deg C, ', hourRH, '% ', hourWindAvr, 'km/hr, ', hourLux, 'Lux')

    # Solar Radiation
    solarRadiation = hourLux * config.luminousEff * (3600/1e6) # (MJ/m^2-hr)

    outgoingRadiation = 0 # equation 39 but am assuming this is small
    netRadiation = ((1 - .23) * solarRadiation) -  outgoingRadiation # equation 38 gives the .23 constant
    if printFactor is True: print('netRadiation: ', '{:3.6f}'.format(netRadiation))

    #Ground Heat Flux
    if hourLux > 3000:
        soilHeatFlux = .1 * netRadiation  # Daytime Gn MJ/m^-hr
    else:
        soilHeatFlux = .5 * netRadiation  # Night Gn MJ/m^-hr

    #psychometric constant is .067 at sea level and .060 at 3000 feet in kPa/deg C
    psychometricConstant = .0665 # (kPa/deg C)

    # e sub zero(T)  saturation vapor pressure at air temp T
    saturationVaporPressure = .6108 * (math.exp((17.27 * hourTemp)/(hourTemp + 273))) # (kPa/deg C)


    # saturation slope vapor pressure at air temperature
    saturationVaporSlope = (4098 * saturationVaporPressure) / ((hourTemp +237.3)**2) # KPa/deg C

    vaporPressure = saturationVaporPressure * (hourRH/100) # e sub a kPa
    windSpeed = hourWindAvr * .278  # wind speed converted to m/sec

    # Penman Monteith Equation in three parts then the whole
    solarComponent = ((.408 * saturationVaporSlope) * (netRadiation - soilHeatFlux))
    if printFactor is True: print('solar component: ', '{:4.3f}'.format(solarComponent))

    windComponent = (psychometricConstant * (37 / (hourTemp + 273))) * windSpeed * (saturationVaporPressure - vaporPressure)
    if printFactor is True: print('wind component: ', '{:4.3f}'.format(windComponent))

    workingDenominator = saturationVaporSlope + (psychometricConstant * (1 + (.34 * windSpeed)))
    if printFactor is True: print('denominator: ', '{:4.3f}'.format(workingDenominator))
    if printFactor is True: print('')

    # final Penman-Monteith
    evapoTranspiration = (solarComponent + windComponent) / workingDenominator

    return evapoTranspiration  # mm of water lost in that one hour
```


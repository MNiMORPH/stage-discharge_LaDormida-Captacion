#! /usr/bin/python3

# Plot the cross section at the La Dormida Captación gauging site
# Data collected by Crystal Ng and Daniel Stanton

# A. Wickert

import pandas as pd
from matplotlib import pyplot as plt
from shapely.geometry import LineString, Point
import numpy as np

df = pd.read_csv('LD-Cap_x-sec.csv')

monR = df[df['Description'] == 'right monument (floodplain)']
monL = df[df['Description'] == 'left monument']

baseline = LineString( [ monL[ ['Easting', 'Northing'] ].values.squeeze(),
                         monR[ ['Easting', 'Northing'] ].values.squeeze() ] )

EN = np.array( df[['Easting', 'Northing']] )

distanceLR = []
for row in EN:
    p = Point( row )
    dist = baseline.project(p)
    distanceLR.append(dist)

df['Distance LR'] = distanceLR

# Figure size for HESS. 1-col = 8.3 cm
#cm = 1/2.54

plt.figure( figsize=(8.3/1.5, 5/1.5) )
plt.plot( df['Distance LR'], df['Elevation'] - monL['Elevation'].iloc[0],
            color='.2', linewidth=2 )

plt.xlabel('Distance from river-left monument [m]', fontsize=14)
plt.ylabel('Elevation from\nriver-left monument [m]', fontsize=14)
plt.tight_layout()

"""
# Plotting strangely & not needed
waterL = df[ df['Description'] == 'left edge' ]
waterR = df[ df['Description'] == 'right water edge/bank' ]

waterLR = pd.concat( [waterL, waterR] )
plt.plot( waterLR['Distance LR'],
            waterLR['Elevation'] - monL['Elevation'].iloc[0],
            color='darkblue', linewidth=2 )
"""

plt.savefig('LDCap_XS.pdf')

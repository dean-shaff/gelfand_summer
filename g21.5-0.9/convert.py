#converting from kilometers/s to mas/yr

from astropy import units as u 

distance = float(raw_input("Distance? "))*u.kpc
distance = distance.to(u.km)
input1 = float(raw_input("Km/s? "))
input1 *= u.km
input1 = input1/distance
input1 *= u.rad/u.second
print(input1.to(u.mas/u.yr))

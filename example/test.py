from epanet import toolkit
from epanet_tools import project

from epanet_tools import calibration_data


cal_data = calibration_data.load_calibration("calibration.txt")


print(cal_data)

exit()

p = Project()
p.open('Net3.inp')


p.set_network_attribute("links[20].roughness", 200)
p.set_network_attribute("nodes[10].elevation", 550)

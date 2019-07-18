from epanet import toolkit

from project import Project

p = Project()
p.open('Net3.inp')


p.set_network_attribute("links[20].roughness", 200)
p.set_network_attribute("nodes[10].elevation", 550)


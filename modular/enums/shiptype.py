import copy
from  enum import Enum, unique

class ShipType(Enum):
    Airfreight = 1
    Airlift = 2
    General = 3
    Seaway = 4
    Sample = 5
    MoveStorage = 6
    Railway = 7
    Ground = 8
    Vessel = 9
    ExpressGround = 10
    SeawayFCL = 11
    SeawayLCL = 12
    RailwayFCL = 13
    RailwayLCL = 14
    VesselFCL = 15
    VesselLCL = 16
    GroundFCL = 17
    GroundLCL = 18
__ship_type_option = [ str(x.value)+'-'+x.name  for x in ShipType]

def ship_type_option_enum():

    # return copy.deepcopy(__ship_type_option)
    return copy.deepcopy(__ship_type_option)

if __name__=="__main__":
    print(ShipType.Vessel)
    print(ShipType(1).name)
    print(ShipType['Seaway'].value)
    print(ShipType['Seaway'])

    b = ship_type_option_enum()
    b[0] = 'xxx'
    print(ship_type_option_enum())
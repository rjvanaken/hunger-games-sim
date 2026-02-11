import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from Tribute import Tribute
from Resource import Resource


# setup
T2 = Tribute(id=21, pos=(5, 5))
T1 = Tribute(id=2, pos=(5, 5))

R1 = Resource(1, (5, 5), 1)
R2 = Resource(1, (5, 5), 2, 15)
R3 = Resource(1, (5, 5), 3, 1)
R4 = Resource(1, (5, 5), 4)
R5 = Resource(1, (5, 5), 5, 10)
R6 = Resource(1, (5, 5), 6)
R7 = Resource(1, (5, 5), 7)


def test_tribute_creation_attributes():
    
    assert T1.pos == (5, 5)
    assert T1.id == 2
    assert T1.letter.upper() == 'C'
    assert T2.letter.upper() == 'V'
    assert T1.district == 2
    assert T2.district == 11
    assert T1.health == 100
    assert T1.thirst == 100
    assert T1.hunger == 100
    assert T1.water_supply == 0
    assert T1.max_water == 0
    assert T1.food == 0
    assert T1.medical == 0
    assert T1.capacity == 2
    assert T1.inventory == 0
    assert T1.weapon_value == 0
    assert T1.isAlive == True
    
    assert T1.gender == 'male'
    assert T2.gender == 'female'



def testPickup():

    T1.pickUpResource(R6)
    assert T1.capacity == 7
    assert T1.food == 2
    assert T1.max_water == 15
    assert T1.inventory == 3

    T1.pickUpResource(R2)
    assert T1.max_water == 30
    assert T1.inventory == 4

    T1.pickUpResource(R3)
    assert T1.food == 3
    assert T1.inventory == 5

    T1.pickUpResource(R4)
    assert T1.medical == 1
    assert T1.inventory == 6

    T1.pickUpResource(R5)
    assert T1.strength == 10
    assert T1.inventory == 7

    T1.pickUpResource(R2)
    assert T1.max_water == 30
    assert T1.inventory == 7

    T1.water_supply = 3
    T1.pickUpResource(R1)
    assert T1.water_supply == T1.max_water

    T2.pickUpResource(R7)
    assert T2.capacity == 12
    assert T2.medical == 1













def main():
    test_tribute_creation_attributes()
    testPickup()


if __name__ == '__main__':
    main()  
    
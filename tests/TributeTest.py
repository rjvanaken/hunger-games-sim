import sys
import os
import random
import math

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from config import BASE_DAMAGE, STRENGTH_MULTIPLIER, WATER_VALUE, FOOD_VALUE, MEDICAL_VALUE, CANTEEN_VALUE
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
    assert T1.max_strength == T1.strength
    
    assert T1.gender == 'male'
    assert T2.gender == 'female'



def testGetRandomAge():
    for i in range(50):
        assert T1.getRandomAge() >= 12
        assert T1.getRandomAge() <= 18


def testPickup():

    T1.pickUpResource(R6)
    assert T1.capacity == 7
    assert T1.food == 2
    assert T1.max_water == 15
    assert T1.inventory == 3

    old = T1.max_water
    T1.pickUpResource(R2)
    assert T1.max_water == old + CANTEEN_VALUE
    assert T1.inventory == 4

    T1.pickUpResource(R3)
    assert T1.food == 3
    assert T1.inventory == 5

    T1.pickUpResource(R4)
    assert T1.medical == 1
    assert T1.inventory == 6

    T1.strength = 0
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


    T2.inventory = T2.capacity
    assert T2.pickUpResource(R3) == "storage capacity reached. cannot pick up new item"


    # tests can pickup water from source when inventory is full 
    T2.max_water = 20
    T2.water_supply = 7
    assert T2.water_supply == 7
    T2.pickUpResource(R1)
    assert T2.water_supply == 20



def testEat():
    T1.inventory = 10
    T1.food = 3 
    T1.hunger = 10
    

    old_hunger = T1.hunger
    T1.eatFood()
    assert T1.hunger == old_hunger + FOOD_VALUE
    assert T1.food == 2
    T1.inventory = 9

    T1.hunger = 99
    T1.eatFood()
    assert T1.hunger == 100
    assert T1.food == 1
    T1.inventory = 8

    T1.eatFood()
    assert T1.hunger == 100
    assert T1.food == 1
    T1.inventory = 8



def testDrink():
    T1.inventory = 10
    T1.water_supply = 3 
    T1.thirst = 20
    
    old_thirst = T1.thirst
    T1.drinkWater()
    assert T1.thirst == old_thirst + WATER_VALUE
    assert T1.water_supply == 2

    T1.thirst = 99
    T1.drinkWater()
    assert T1.thirst == 100
    assert T1.water_supply == 1

    T1.drinkWater()
    assert T1.thirst == 100
    assert T1.water_supply == 1
    



def testUseMedical():
    T1.inventory = 10
    T1.medical = 3 
    T1.health = 10
    

    old_health = T1.health
    T1.useMedical()
    assert T1.health == old_health + MEDICAL_VALUE
    assert T1.medical == 2
    T1.inventory = 9

    T1.health = 99
    T1.useMedical()
    assert T1.health == 100
    assert T1.medical == 1
    T1.inventory = 8

    T1.useMedical()
    assert T1.health == 100
    assert T1.medical == 1
    T1.inventory = 8

    


def testSetTributeStatus():

    T1.health = 100
    T1.setTributeStatus()
    assert T1.isAlive == True
    T1.health = 0
    T1.setTributeStatus()
    assert T1.isAlive == False


    T2.health = 100
    T2.setTributeStatus()
    assert T2.isAlive == True
    T2.health = -5
    T2.setTributeStatus()
    assert T2.isAlive == False


def testAttackSubtractsHealth():
    T1.strength = 40
    T2.strength = 30
    T1.health = 100
    T2.health = 100

    T2_health = T2.health
    random.seed(42)
    T1.attack(T2)
    assert T2.health == T2_health - (BASE_DAMAGE + int(math.ceil((T1.strength * STRENGTH_MULTIPLIER))))
    assert T1.health == 100





def main():
    testGetRandomAge()
    test_tribute_creation_attributes()
    testPickup()
    testEat()
    testDrink()
    testUseMedical()
    testSetTributeStatus()
    testAttackSubtractsHealth()


if __name__ == '__main__':
    main()  
    
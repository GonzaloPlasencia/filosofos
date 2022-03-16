
"""
@author: Gonzalo Plasencia Boticario
"""

from multiprocessing import Process, \
  BoundedSemaphore, Semaphore, Lock, Condition,\
  current_process, \
  Value, Array, Manager
from time import sleep
from random import random

class Table():
    def __init__(self, nphil:int,manager):
        self.mutex=Lock()
        self.numphil=nphil
        self.phil=None
        self.listphil=manager.list([False for _ in range(nphil)])
        self.freefork=Condition(self.mutex)
        self.neating=Value('i',0)
        self.nthinking=Value('i',nphil)
        
    def set_current_phil(self,num):
        self.phil=num
             
    def freefork_num(self):
        return not(max(self.listphil[(self.phil-1)%self.numphil],self.listphil[(self.phil+1)%self.numphil]))
    
    def wants_eat(self,num):
        self.mutex.acquire()
        self.freefork.wait_for(self.freefork_num)
        self.listphil[num]=True
        self.neating.value+=1
        self.nthinking.value-=1
        self.mutex.release()
        
    def wants_think(self, num):
        self.mutex.acquire()
        self.listphil[num]=False
        self.neating.value-=1
        self.nthinking.value+=1
        self.freefork.notify_all()
        self.mutex.release()
        
        
        
class CheatMonitor():
    def __init__(self):
        self.mutex=Lock()
        self.numeat=Value('i',0)
        self.othereat=Condition(self.mutex)
        
    def othereating(self):
        return self.numeat.value==2
        
    def is_eating(self,num):
        self.mutex.acquire()
        self.numeat.value+=1
        self.othereat.notify_all()
        self.mutex.release()
        
    def wants_think(self,num):
        self.mutex.acquire()
        self.othereat.wait_for(self.othereating)
        self.numeat.value-=1
        self.othereat.notify_all()
        self.mutex.release()
        
        
    
class AnticheatTable():
    def __init__(self, nphil:int,manager):
        self.mutex=Lock()
        self.numphil=nphil
        self.phil=None
        self.listphil=manager.list([False for _ in range(nphil)])
        self.listhungry=manager.list([False for _ in range(nphil)])
        self.freefork=Condition(self.mutex)
        self.chungry=Condition(self.mutex)
        self.neating=Value('i',0)
        self.nthinking=Value('i',nphil)
        
    def set_current_phil(self,num):
        self.phil=num
             
    def freefork_num(self):
        return not(max(self.listphil[(self.phil-1)%self.numphil],self.listphil[(self.phil+1)%self.numphil]))
    
    def next_not_hungry(self):
        return not(self.listhungry[(self.phil+1)%self.numphil])
    
    def wants_eat(self,num):
        self.mutex.acquire()
        self.chungry.wait_for(self.next_not_hungry)
        self.listhungry[num]=True
        self.freefork.wait_for(self.freefork_num)
        self.listphil[num]=True
        self.neating.value+=1
        self.nthinking.value-=1
        self.mutex.release()
        
    def wants_think(self, num):
        self.mutex.acquire()
        self.listhungry[num]=False
        self.listphil[num]=False
        self.neating.value-=1
        self.nthinking.value+=1
        self.freefork.notify_all()
        self.chungry.notify_all()
        self.mutex.release()   
 










       
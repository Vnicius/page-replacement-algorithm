#!/usr/bin/python
#-*- coding : utf-8 -*-

############################
# Page Replacement Algorithms
# Author: Vinícius Matheus (github.com/vnicius)
############################

import sys
import copy
import math

def fifo(ram_size, seq_pages):
    """FIFO Algorithm"""
    ram = [None] * ram_size
    seq = copy.deepcopy(seq_pages)
    faults = 0
    frame_victim = 0

    for page in seq:
        if page in ram:     #see if the page is in the ram
            continue

        ram[frame_victim] = page    #set new page on the frame
        frame_victim = (frame_victim + 1) % ram_size
        faults += 1

    print("FIFO: "+str(faults))

def otm(ram_size,seq_pages):
    """Optimal Algorithm"""
    ram = [None] * ram_size
    seq = copy.deepcopy(seq_pages)
    faults = 0
    frame_victim = 0
    page = 0

    for p in range(len(seq_pages)):
        page = seq_pages[p]

        if page in ram:     #see if the page is in the ram
            continue
        elif None in ram:   #if has a empty space in ram
            ram[ram.index(None)] = page
            faults += 1
            continue

        aux = [math.inf] * ram_size    #axiliar array with next pages calls values
        larger = 0      #the larger diff

        for pg in range(p+1,len(seq_pages)):    #the rest of page in the sequence
            for i in range(ram_size):
                #if is the first ocorrence of the page in the sequence
                if (aux[i] == math.inf) and (seq_pages[pg] == ram[i]):
                    aux[i] = pg - p    #diff until the next occurrence in the sequence

        for i in range(ram_size):
            if aux[i] > larger:
                larger = aux[i]
                frame_victim = i

        ram[frame_victim] = page    #set the new page on the frame victim
        faults += 1     #incr faults

    print("OTM "+str(faults))

def lru(ram_size,seq_pages):
    """LRU Algorithm"""
    ram = [None] * ram_size
    seq = copy.deepcopy(seq_pages)
    faults = 0
    frame_victim = 0
    current_clock = 0
    clocks = [0] * ram_size

    for page in seq:
        if page in ram:     #see if the page is in the ram
            clocks[ram.index(page)] = current_clock
            current_clock += 1
            continue
        elif None in ram:
            index = ram.index(None)     #search the next free frame
            ram[index] = page       #set the page in the free frame
            clocks[index] = current_clock   #set the current clock in th same position
            faults += 1
            current_clock += 1
            continue

        lr = current_clock      #last recent

        for i in range(ram_size):
            if clocks[i] < lr:
                lr = clocks[i]
                frame_victim = i

        ram[frame_victim] = page
        clocks[frame_victim] = current_clock
        faults += 1
        current_clock += 1

    print("LRU: "+str(faults))

##################################

if __name__ == "__main__":
    name = sys.argv[1]  #file in name
    fl = open(name,"r")
    ram_size = 0    #size of the ram
    seq_pages = []  #sequence of the pages access

    lines = fl.readlines()  #read lines
    fl.close()

    ram_size = int(lines[0].replace("\n",""))   #first line is the ram size

    for line in lines[1:]:
        seq_pages.append(int(line.replace("\n","")))

    fifo(ram_size,seq_pages)    #call FIFO Algorithm
    otm(ram_size,seq_pages)     #call Optimal Algorithm
    lru(ram_size,seq_pages)     #call LRU Algorithm

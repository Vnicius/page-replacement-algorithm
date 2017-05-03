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
    ram = [0]*ram_size
    seq = copy.deepcopy(seq_pages)
    page_table = [] #[page_number,validation_bit]
    ocup = 0
    faults = 0
    frame_victim = 0

    for page in seq:
        #print(page)
        if ocup < ram_size:  #if the ram is not full
            for i in range(len(ram)):   #search for the next frame free
                if ram[i] == 0:
                    ram[i] = page
                    break

            page_table.append([page,True])   #add page in page table
            ocup += 1   #incr number of frames full in ram
            faults += 1  #incr number of page faults
            #print("page_table: "+str(page_table)+"\nram: "+str(ram)+"\n\n")
        else:
            if in_ram(page,page_table):     #see if the page is in the ram
                continue

            if not in_page_table(page,page_table):  #if the page is in the page table
                page_table.append([page,True])

            page_victim = ram[frame_victim]     #get the page victim
            ram[frame_victim] = page    #set new page on the frame

            for i in range(len(page_table)):    #uptade the frame the valiable bits on the page table
                if page_table[i][0] == page_victim:
                    page_table[i][1] = False
                elif page_table[i][0] == page:
                    page_table[i][1] = True

            if (frame_victim+1) != ram_size:
                frame_victim += 1
            else:       #if the next frame pass the ram size
                frame_victim = 0

            faults += 1
            #print("page_table: "+str(page_table)+"\nram: "+str(ram)+"\n\n")

    print("FIFO: "+str(faults))

def otm(ram_size,seq_pages):
    """Optimal Algorithm"""
    ram = [0]*ram_size
    seq = copy.deepcopy(seq_pages)
    page_table = []  #[page_number,valiable_bit]
    ocup = 0
    faults = 0
    frame_victim = 0
    page = 0

    for p in range(len(seq_pages)):
        page = seq_pages[p]
        #print(page)
        if ocup < ram_size:  #if the ram is not full
            for i in range(len(ram)):   #search for the next frame free
                if ram[i] == 0:
                    ram[i] = page
                    break

            page_table.append([page,True])   #add page in page table
            ocup += 1   #incr number of frames full in ram
            faults += 1  #incr number of page faults
            #print("page_table: "+str(page_table)+"\nram: "+str(ram)+"\n\n")
        else:
            if in_ram(page,page_table):     #see if the page is in the ram
                continue

            if not in_page_table(page,page_table):  #if the page is in the page table
                page_table.append([page,False])

            aux = []    #axiliar array

            for pg in range(len(page_table)):   #array with pages in the memory
                if page_table[pg][1]:
                    aux.append([page_table[pg][0],math.inf])   #[page_number,nex_call]

            for pg in range(p+1,len(seq_pages)):    #the rest of page in the sequence
                for i in range(len(aux)):
                    #if is the first ocorrence of the page int the sequence
                    if (aux[i][1] == math.inf) and (seq_pages[pg] == aux[i][0]):
                        aux[i][1] = pg - p    #diff unil the next ocorrence in the sequence

            larger = 0      #the larger diff
            page_victim = 0

            for pg in range(len(aux)):  #search the page with the larger diff
                if aux[pg][1] > larger:
                    larger = aux[pg][1]
                    page_victim = aux[pg][0]    #set the page victim

            for f in range(len(ram)):   #search the frame victim
                if page_victim == ram[f]:
                    frame_victim =  f
                    break

            ram[frame_victim] = page    #set the new page on the frame victim

            for pg in range(len(page_table)):
                if page_table[pg][0] == page_victim:
                    page_table[pg][1] = False    #set valiable bit in the page victim on page table
                elif page_table[pg][0] == page:
                    page_table[pg][1] = True     #set valiable bit in the new page on page table

            #print("page_table: "+str(page_table)+"\nram: "+str(ram)+"\n\n")
            faults += 1     #incr faults

    print("OTM "+str(faults))

def in_ram(page_num,page_table):
    for pg in page_table:
        if pg[0] == page_num:
            return pg[1]
    return False

def in_page_table(page_num,page_table):
    for pg in page_table:
        if pg[0] == page_num:
            return True
    return False

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
    otm(ram_size,seq_pages)

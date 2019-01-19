# -*- coding: utf-8 -*-
import networkx as nx
import os

#sign asn relationship with two file
def get_input_file(as_rel_f, as_link_f, out_file):
    #get as rel dic
    as_dic = {}
    rel_f = open(as_rel_f, 'r')
    for line in rel_f:
        if "#" in line:
            continue
        cut = line.strip().split('|')
        if len(cut) != 3:
            print [line]
            continue
        as1 = cut[0]
        as2 = cut[1]
        rel = cut[2]
        if rel == "-1":
            if as1 not in as_dic:
                as_dic[as1] = {}
                as_dic[as1]["p2c"] = set()
                as_dic[as1]["c2p"] = set()
                as_dic[as1]["p2p"] = set()   
            if as2 not in as_dic:
                as_dic[as2] = {}
                as_dic[as2]["p2c"] = set()
                as_dic[as2]["c2p"] = set()
                as_dic[as2]["p2p"] = set()   
            as_dic[as1]["p2c"].add(as2)
            as_dic[as2]["c2p"].add(as1)
        if rel == "0":
            if as1 not in as_dic:
                as_dic[as1] = {}
                as_dic[as1]["p2c"] = set()
                as_dic[as1]["c2p"] = set()
                as_dic[as1]["p2p"] = set()   
            if as2 not in as_dic:
                as_dic[as2] = {}
                as_dic[as2]["p2c"] = set()
                as_dic[as2]["c2p"] = set()
                as_dic[as2]["p2p"] = set() 
            as_dic[as1]["p2p"].add(as2)
            as_dic[as2]["p2p"].add(as1)
    rel_f.close()
    #mark links file by as_rel
    link_f = open(as_link_f, 'r')
    out_f = open(out_file, 'w')
    for line in link_f:
        cut = line.strip().split()
        if len(cut) != 2:
            print [line]
            continue
        as1 = cut[0]
        as2 = cut[1]
        if as1 in as_dic:
            rel = 0
            if as2 in as_dic[as1]["p2c"]:
                rel = "p2c"
            if as2 in as_dic[as1]["c2p"]:
                rel = "c2p"
            if as2 in as_dic[as1]["p2p"]:
                rel = "p2p"
            if rel != 0:
                out_f.write(line.strip() + ' ' + rel + '\n')
    link_f.close()
    out_f.close()



def main(as1, as2):
    get_input_file("as_rel_test1.txt", "as_links1.txt", "as_links_rel.txt")
    
    pass

if __name__ == "__main__":
    main("1","2")
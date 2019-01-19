# -*- coding: utf-8 -*-
import networkx as nx
import os

def comprae_len(a1, a2):
    if len(a1) > len(a2):
        return 1
    elif len(a1) == len(a2):
        return 0
    else:        
        return -1

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
            else:
                # out_f.write(line.strip() + ' ' + "p2p" + '\n')
                pass
        else:
            # out_f.write(line.strip() + ' ' + "p2p" + '\n')
            pass

    link_f.close()
    out_f.close()

def get_graph():
    global G
    G = nx.Graph()
    f = open("as_links_rel.txt")
    for line in f:
        cut = line.strip().split()
        as1 = cut[0]
        as2 = cut[1]
        rel = cut[2]
        G.add_edge(int(as1), int(as2), r = rel)
    f.close()
    # print G.edges(data=True)
    # print [G[684119][174]["r"]]

def is_valley_free(path):
    rel_path = []
    for i in range(len(path)-1):
        rel_path.append(G[path[i]][path[i+1]]["r"])
    valley_free = True
    p2p = 0
    p2c = 0
    for rel in rel_path:
        if p2c == 1:
            if rel == "c2p" or rel == "p2p":
                valley_free = False
                break 
        if p2p == 1:
             if rel == "c2p" or rel == "p2p":
                valley_free = False
                break        
        if rel == "p2p":
            p2p = 1
        if rel == "p2c":
            p2c = 1
    return valley_free

def get_shortest_path(as1, as2):
    as1 = int(as1)
    as2 = int(as2)
    #node not in graph
    if (not G.has_node(as1)) or (not G.has_node(as2)):
        return "has_no_path"
    #don't have path
    if not nx.has_path(G, as1, as2):
        return "has_no_path"
    #use shortest paths alo. 
    # if one of shortest paths is valley-free, return all valley-free shortest paths
    print "get shortest path"
    ret_path = set()
    shortest_paths = list(nx.all_shortest_paths(G, source=as1, target=as2))
    print len(shortest_paths)
    print len(shortest_paths[0])
    for path in shortest_paths:
        print path
    for path in shortest_paths:
        if is_valley_free(path):
            ret_path.add(path)
    if len(ret_path) != 0:
        return ret_path
    else:
        print "all shortest paths are not valley-free"
        # if shortest paths is not valley-free
        # get all simple paths from short to long
        print "get all simple paths"
        all_simple_paths = list(nx.all_simple_paths(G, source=as1, target=as2, cutoff=10))
        print len(all_simple_paths)
        all_simple_paths.sort(cmp=comprae_len)
        shortest_valley_free_len = 0
        for path in all_simple_paths:
            if shortest_valley_free_len == 0:
                if is_valley_free(path):
                    shortest_valley_free_len = len(path)
                    ret_path.add(path)
            else:
                if len(path) > shortest_valley_free_len:
                    break
                else:
                    if len(path) == shortest_valley_free_len:
                        if is_valley_free(path):
                            ret_path.add(path)

        if shortest_valley_free_len != 0:
            return ret_path
        else:
            #if all simple paths is not valley-free
            return "has_no_path"

def main(as1, as2):
    # get_input_file("as_rel.txt", "all_links.txt", "as_links_rel.txt")
    get_graph()
    print "graph creat finish"
    ret = get_shortest_path(as1,as2)
    if ret == "has_no_path":
        print ret
    else:
        print len(ret)

if __name__ == "__main__":
    G = nx.Graph()
    main(12414, 7500)
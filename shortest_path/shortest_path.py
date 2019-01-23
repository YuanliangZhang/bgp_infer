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

def get_graph(file_name):
    global G
    G = nx.Graph()
    f = open(file_name, 'r')
    for line in f:
        cut = line.strip().split()
        as1 = cut[0]
        as2 = cut[1]
        rel = cut[2]
        G.add_edge(int(as1), int(as2), r = rel)
    f.close()
    # print list(nx.all_neighbors(G, 174))
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

def list2str(path):
    s = ''
    if len(path) == 0:
        return s
    for node in path:
        s = s + str(node) + ' '
    return s[:-1]

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
    # for path in shortest_paths:
    #     print path
    # return len(shortest_paths)
    # print len(shortest_paths[0])
    for path in shortest_paths:
        if is_valley_free(path):
            ret_path.add(list2str(path))
    if len(ret_path) != 0:
        return ret_path
    else:
        return "shortest paths not valley-free"
    # if len(ret_path) != 0:
    #     return ret_path
    # else:
    #     print "all shortest paths are not valley-free"
    #     # if shortest paths is not valley-free
    #     # get all simple paths from short to long
    #     print "get all simple paths"
    #     all_simple_paths = list(nx.all_simple_paths(G, source=as1, target=as2, cutoff=10))
    #     print len(all_simple_paths)
    #     all_simple_paths.sort(cmp=comprae_len)
    #     shortest_valley_free_len = 0
    #     for path in all_simple_paths:
    #         if shortest_valley_free_len == 0:
    #             if is_valley_free(path):
    #                 shortest_valley_free_len = len(path)
    #                 ret_path.add(path)
    #         else:
    #             if len(path) > shortest_valley_free_len:
    #                 break
    #             else:
    #                 if len(path) == shortest_valley_free_len:
    #                     if is_valley_free(path):
    #                         ret_path.add(path)

    #     if shortest_valley_free_len != 0:
    #         return ret_path
    #     else:
    #         #if all simple paths is not valley-free
    #         return "has_no_path"
def after_add_valley_f(now, i):
    pre_node = prevPoints[now]
    if pre_node == "src":
        return True
    all_path = []
    for pre in pre_node:
        all_path.append([pre, now, i])
    have_valley_free = 0
    for path in all_path:
        if  is_valley_free(path):
            have_valley_free = 1
    if have_valley_free == 0:
        return False
    else:
        return True

def bfs(src, dst):
    global prevPoints
    if (not G.has_node(src)) or (not G.has_node(dst)):
        return False
    distance = {}
    prevPoints = {}
    prevPoints[src] = "src"
    path = {}
    path[src] = 1
    queue = []
    queue.append(src)
    while len(queue) != 0:
        now = queue.pop(0)
        if now not in distance:
            distance[now] = 0
        dis = distance[now] + 1
        all_neighbor = list(nx.all_neighbors(G, now))
        custom = []
        provide = []
        peer = []
        neighbor_queue = []
        for neighbor in all_neighbor:
            if G[now][neighbor]["r"] == 'p2c':
                custom.append(neighbor)
            if G[now][neighbor]["r"] == 'c2p':
                provide.append(neighbor)
            if G[now][neighbor]["r"] == 'p2p':
                peer.append(neighbor)
        for c in custom:
            neighbor_queue.append(c)
        for p in provide:
            neighbor_queue.append(p)
        for p in peer:
            neighbor_queue.append(p)
        for i in neighbor_queue:
            if i not in distance:
                distance[i] = 0
            if (distance[i] == 0 and after_add_valley_f(now,i)) or (distance[i] > dis and after_add_valley_f(now,i)):
                distance[i] = dis
                if i not in path:
                    path[i] = 0
                if now not in path:
                    path[now] = 0
                path[i] = path[now]
                queue.append(i)
                prevPoints[i] = []
                prevPoints[i].append(now)
            elif i in distance:
                if (distance[i] == dis and after_add_valley_f(now,i)):
                    if i not in path:
                        path[i] = 0
                    if now not in path:
                        path[now] = 0
                    path[i] += path[now]
                    if i not in prevPoints:
                        prevPoints[i] = []
                    prevPoints[i].append(now)
    return True
def getPaths(start, index):
    childPaths = []
    midPaths = []
    if index != start:
        for i in range(len(prevPoints[index])):
            childPaths = getPaths(start, prevPoints[index][i])
            for j in range(len(childPaths)):
                childPaths[j].append(index)
            if len(midPaths) == 0:
                midPaths = childPaths
            else:
                for node in childPaths:
                    midPaths.append(node)
    else:
        midPaths.append([start])
    return midPaths

def return_valley_free_path(path_list):
    all = set()
    for path in path_list:
        if is_valley_free(path):
            all.add(list2str(path))
    if len(all) != 0:
        return all
    else:
        return "no result"

def main(as1, as2):
    as1 = int(as1)
    as2 = int(as2)
    # get_input_file("as_rel.txt", "all_links.txt", "as_links_rel_ori.txt")
    get_graph("as_links_rel_ori.txt")
    all_path = get_shortest_path(as1, as2)
    if type(all_path) == str:
    # if 1:
        ret = bfs(as1, as2)
        if ret == True:
            all_path = return_valley_free_path(getPaths(as1, as2))
        else:
            all_path = "no result"
    print all_path
  

if __name__ == "__main__":
    G = nx.Graph()
    main(12307, 7500)
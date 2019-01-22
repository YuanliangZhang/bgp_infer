# as shortest paths algorithm which is valley-free
* all_links.txt is all as links
* as_rel.txt is all as relationship
* shortest_path.py:
When weight is 1, Dijkstra can be bfs which add juedge for shortest length of path.
I first juedge whether shortest path with networkx has valley-free path, if not use bfs().
When bfs() add a list **prevPoints** record all precursors node.
After bfs(), dfs() use **prevPoints** get all path.
# reference:
* [shortest path when weight is 1](https://blog.csdn.net/thinkerleo1997/article/details/77916039)
* [how to get all shortest path]()https://blog.csdn.net/u013615687/article/details/69062803
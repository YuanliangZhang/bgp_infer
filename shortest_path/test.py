f = open("as_links_rel_ori.txt", 'r')
f1 = open("as_links_rel.txt", 'w')
i = 0
for line in f:
    f1.write(line)
    i += 1
    if i == 10000:
        break
f.close()
f1.close()

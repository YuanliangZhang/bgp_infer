import pymysql
import re
def main():
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='1q2w3e4r', db='bgp_data')
    cursor = db.cursor()
    # get messages msg_md5
    sql = "select as1,as2 from links"
    cursor.execute(sql)
    links_res = cursor.fetchall()
    print len(links_res)
    links_set = set()
    for link in links_res:
        links_set.add((link[0],link[1]))
    f = open("all_links.txt", 'w')
    for link in links_set:
        is_num_1 = re.match(r"\d+$",link[0])
        is_num_2 = re.match(r"\d+$",link[1])
        if is_num_1 and is_num_2:
            f.write(link[0] + ' ' + link[1] + '\n')
    f.close()
    db.commit()
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()

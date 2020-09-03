#coding=utf-8                                                                   
'''
    author:the5fire
    blog:http://www.the5fire.com
    date:2012-07-03
'''

import time

def writefile():
    counter = 0 
    while True:
        writefile = open("file/test.txt", 'a')
        writefile.write('test' + str(counter) + '\n')
        writefile.close()
        writefile2 = open("file/test2.txt", 'a')
        writefile2.write('zzz' + str(counter) + '\n')
        writefile2.close()
        counter += 1
        print  counter
        time.sleep(2)

if __name__ == '__main__':
    # import sys 
    # if len(sys.argv) == 2:
    #     filename = sys.argv[1]
    writefile()
"""O(n)"""
if __name__ == '__main__':
    list=[2,8,7,2,2,5,2,3,1,2,2]
    for i in list:
        if len(list)/2 <  list.count(i):
            print(i)
            break

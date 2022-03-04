from pathos.helpers import mp
import time
import dill as pickle

def foo(print_me):   
    print(print_me + " foo" + " Start")
    for i in range(10000000) : pass
    print(print_me + " foo" + " Stop")
    with open("angle.pkl", "wb") as file:
        pickle.dump('a', file)

def foo2(print_me):   
    print(print_me + " foo2" + " Start")
    for i in range(10000000) : pass
    print(print_me + " foo2" + " Stop")
    with open("pos.pkl", "wb") as file:
        pickle.dump('b', file)

if __name__ == '__main__':
    start_time = time.time()
    # process = [mp.Process(target=foo, args=("HI",)),mp.Process(target=foo2, args=("HI2",))]
    # r1 = map(lambda p: p.start(), process) 
    # r2 = map(lambda p: p.join(), process) 
    # r1 = list(r1)
    # r1 = list(r2)
    p1 = mp.Process(target=foo, args=("HI",))
    p1.start()
    p2 = mp.Process(target=foo2, args=("HI2",))
    p2.start()
    p1.join()
    p2.join()
    a = pickle.load(open("angle.pkl","rb"))
    b = pickle.load(open("pos.pkl","rb"))
    print(a, b)
    print("--- %s seconds for parallel ---" % (time.time() - start_time))

    start_time = time.time()
    print('HI' + " foo" + " Start")
    for i in range(10000000) : pass
    print('HI' + " foo" + " Stop")
    print('HI2' + " foo2" + " Start")
    for i in range(10000000) : pass
    print('HI2' + " foo2" + " Stop")
    print(a,b)
    print("--- %s seconds for sequential ---" % (time.time() - start_time))

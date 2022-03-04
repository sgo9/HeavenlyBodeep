import multiprocessing as mp
import mediapipe as mlp
holistic = mp.solutions.holistic.Holistic(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5)

def func1(return_dict):
    print('func1: starting')
    for i in range(100000000): pass
    print('func1: finishing')
    holistic.process()
    return_dict['positions'] = 'pos_complex'

def func2(return_dict):
    print('func2: starting')
    for i in range(100000000): pass

    print('func2: finishing')
    return_dict['angle'] = 18

if __name__ == '__main__':
    manager = mp.Manager()
    return_dict = manager.dict()    
    p1 = mp.Process(target=func1, args=(return_dict,))
    p1.start()
    p2 = mp.Process(target=func2, args=(return_dict,))
    p2.start()
    p1.join()
    p2.join()
    print(return_dict)
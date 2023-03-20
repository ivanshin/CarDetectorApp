import sys
sys.path.append('D:\\Projects\\Python\\CarDetector')

import requests
import io
from PIL import Image
from model_utils import model_utils as mu
from model.segnet import torch
from fastapi import status


def test_device_usage():
    DEVICE = mu.choose_device()
    return 'Device usage'


def test_init_model():
    model = mu.init_model(torch.device('cpu'))
    return 'Model initialization'


def global_test():
    tests = [test_device_usage, test_init_model]
    cntr = 0
    try:
        for i in range(len(tests)):
            #tests[i]()
            print(f'# {tests[i]()} --- passed!')
            cntr=i + 1
    except:
        print(f'# {tests[i]()} --- failed!!!')
    finally:
        print(f' --- Total tests passed: {cntr/len(tests) * 100:.1f}% --- ')

global_test()






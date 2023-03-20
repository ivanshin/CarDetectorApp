import requests


def test_upload_image():
    url = 'http://127.0.0.1:8000/predict'
    file = {'file': open('webp/assets/test_1.jpg', 'rb')}
    resp = requests.post(url=url, files=file)
    return 'POST image png/jpeg'


def test_index():
    url = 'http://127.0.0.1:8000/'
    resp = requests.get(url=url)
    return 'GET index'


def global_test():
    tests = [test_upload_image, test_index]
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
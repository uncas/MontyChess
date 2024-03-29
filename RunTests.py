import sys
import time
import unittest

sys.path.append("src")

def Test(pattern):
    time1 = time.time()
    suite = unittest.TestLoader().discover("test", pattern)
    result = unittest.TestResult()
    suite.run(result)
    print(result)
    for failure in result.failures:
        print(failure)
    for error in result.errors:
        print(error)
    time2 = time.time()
    print("Test duration: " + str(time2-time1) + " seconds")

def TestFast():
    Test("test_*.py")

def TestSlow():
    Test("testslow_*.py")

if __name__ == "__main__":
    TestFast()

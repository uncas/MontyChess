import time
import unittest

if __name__ == "__main__":
    time1 = time.time()
    suite = unittest.TestLoader().discover(".")
    result = unittest.TestResult()
    suite.run(result)
    print(result)
    for failure in result.failures:
        print(failure)
    for error in result.errors:
        print(error)
    time2 = time.time()
    print("Test duration: " + str(time2-time1) + " seconds")

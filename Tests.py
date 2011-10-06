import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover(".")
    result = unittest.TestResult()
    suite.run(result)
    print(result)
    for failure in result.failures:
        print(failure)
    for error in result.errors:
        print(error)

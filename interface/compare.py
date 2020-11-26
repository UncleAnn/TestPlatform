class Compare:

    @staticmethod
    def equal(actual_value, expected_value):
        return actual_value == expected_value

    @staticmethod
    def greater_equal(actual_value, expected_value):
        return actual_value >= expected_value

    @staticmethod
    def lower_equal(actual_value, expected_value):
        return actual_value <= expected_value

    @staticmethod
    def greater(actual_value, expected_value):
        return actual_value > expected_value

    @staticmethod
    def lower(actual_value, expected_value):
        return actual_value < expected_value

    @staticmethod
    def include(actual_value, expected_value):
        return actual_value in expected_value


if __name__ == '__main__':
    compare = Compare()
    assert_list = [
        {'assertType': 'statusCode', 'assertExpr': '$.data.adcode', 'assertCondition': 'equal',
         'assertValue': '320583'},
        {'assertType': 'statusCode', 'assertExpr': '$.data.cross_list.0.weight', 'assertCondition': 'equal',
         'assertValue': '120'}
    ]

    for assert_item in assert_list:
        assert_func = getattr(compare, assert_item['assertCondition'])
        print(assert_func(assert_item['assertExpr'], assert_item['assertValue']))

import pytest
from test_task_folder.app import clean_mongo_field_names as mongo_name

dollar = '\uFF04'
point = '\uFF0E'


def id_func(param):
    return f"{param}"


@pytest.mark.parametrize('input_val, result',
                         [
                             ({"$": "rand_val"}, [("$", dollar)]),
                             ({"$": "$"}, [("$", dollar)]),
                             ({"$$$": "rand_val"}, [("$$$", f"{dollar}$$")]),
                             ({"$rand_key": "rand_val"}, [("$rand_key", f"{dollar}rand_key")])
                         ], ids=id_func)
def test_dollar_as_key_at_start(input_val, result):
    assert mongo_name(input_val) == result


@pytest.mark.parametrize('input_val, result',
                         [
                             ({" $": "rand_val"}, []),
                             ({"rand_key$": "rand_val"}, []),
                         ], ids=id_func)
def test_dollar_as_key_in_the_middle(input_val, result):
    assert mongo_name(input_val) == result


@pytest.mark.parametrize('input_val, result',
                         [
                             ({"rand_key": "$"}, [])
                         ])
def test_dollar_as_value(input_val, result):
    assert mongo_name(input_val) == result


input_dict = {"1_key":
                  {"2_key":
                       {"3_key": {"$": "rand_val"}}}}
input_dict1 = {"$_first":
                   {"$_second": "rand_val"
                    }}


@pytest.mark.parametrize("input_dict, result",
                         [
                             (input_dict, [("$", dollar)]),
                             (input_dict1, [("$_second", f"{dollar}_second"), ("$_first", f"{dollar}_first")])
                         ])
def test_nested_dict(input_dict, result):
    assert mongo_name(input_dict) == result


@pytest.mark.parametrize("input_val, result",
                         [
                             ({dollar: "rand_str"}, [])
                         ])
def test_dollar_as_unicode(input_val, result):
    assert mongo_name(input_val) == result


input_point_dict = {".": "rand_val"}
input_point_dict1 = {".": "."}


@pytest.mark.parametrize("input_val, result",
                         [
                             (input_point_dict, {point: "rand_val"}),
                             (input_point_dict1, {point: "."})
                         ])
def test_point_as_key(input_val, result):
    mongo_name(input_val)
    assert input_val == result


@pytest.mark.parametrize("input_val, expected_dict, result",
                         [
                             ({"$.": "rand_val"}, {f"{dollar}{point}": "rand_val"}, [("$.", f"{dollar}{point}")])
                         ])
def test_point_and_dollar_as_key(input_val, result, expected_dict):
    keys = mongo_name(input_val)
    assert keys == result
    assert input_val == expected_dict
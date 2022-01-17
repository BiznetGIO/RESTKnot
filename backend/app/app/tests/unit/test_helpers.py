import app
from app.helpers import helpers


def test_replace_serial():
    rdata = "ns.example.com. hostmaster.example.com. 2018070410 3600 3600 3600 3600"
    replaced_serial = helpers.replace_serial(rdata, "2020010101")
    assert (
        replaced_serial
        == "ns.example.com. hostmaster.example.com. 2020010101 3600 3600 3600 3600"
    )


def test_increment_serial(monkeypatch):
    monkeypatch.setattr(app.helpers.helpers, "soa_time_set", lambda: "20180704")

    incremented_serial1 = helpers.increment_serial("2018070401")
    assert incremented_serial1 == "2018070402"

    incremented_serial2 = helpers.increment_serial("2018070401", "02")
    assert incremented_serial2 == "2018070403"


def test_exclude_keys():
    my_dict = {"a": 1, "b": 2, "c": 3}
    new_dict = helpers.exclude_keys(my_dict, "a")
    assert new_dict == {"b": 2, "c": 3}

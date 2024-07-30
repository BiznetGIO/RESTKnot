import pytest

from rkapi.app.helpers import validator


def test_valid_ip():
    """This test the valid IP in A and AAAA record"""
    validator.is_valid_ip("2001:db8:10::2")
    validator.is_valid_ip("192.0.2.1")

    with pytest.raises(Exception):
        validator.is_valid_ip("2001:db8:10::2::")
    with pytest.raises(Exception):
        validator.is_valid_ip("192.0.2")
    with pytest.raises(Exception):
        validator.is_valid_ip("270.0.0.2")
    with pytest.raises(Exception):
        validator.is_valid_ip("localhost")


def test_valid_mx():
    validator.is_valid_mx("10 mail.example.com.")
    validator.is_valid_mx("20 mail2.example.com")

    with pytest.raises(Exception):
        validator.is_valid_mx("mail.example.com.")
    with pytest.raises(Exception):
        validator.is_valid_mx("mail2.example.com")


def test_valid_cname():
    validator.is_valid_cname("example")
    validator.is_valid_cname("example.com")
    validator.is_valid_cname("example.com.")
    validator.is_valid_cname("example-one.com")

    with pytest.raises(Exception):
        validator.is_valid_cname("-example")
    with pytest.raises(Exception):
        validator.is_valid_cname("example-")
    with pytest.raises(Exception):
        validator.is_valid_cname("example.-one")
    with pytest.raises(Exception):
        validator.is_valid_cname("example-.one")
    with pytest.raises(Exception):
        validator.is_valid_cname("--example.com.")
    with pytest.raises(Exception):
        validator.is_valid_cname(".example.")
    with pytest.raises(Exception):
        validator.is_valid_cname("*")
    with pytest.raises(Exception):
        validator.is_valid_cname("*.abc")


def test_valid_zone():
    validator.is_valid_zone("example.com")
    validator.is_valid_zone("example-one.com")
    validator.is_valid_zone("example-one-two.com")
    validator.is_valid_zone("mail.example-one.com")
    validator.is_valid_zone("mail.example-one-1.com")
    validator.is_valid_zone("mail.example.com")

    with pytest.raises(Exception):
        validator.is_valid_zone("--example.com.")
    with pytest.raises(Exception):
        validator.is_valid_zone("foo.example.")


def test_valid_soa():
    validator.is_valid_soa(
        "ns.example.com. hostmaster.example.com. 2018070410 3600 3600 3600 3600"
    )

    with pytest.raises(Exception):
        validator.is_valid_soa(
            "ns.example.co hostmaster.example.com. 2018070410 imnotint 3600 3600 3600"
        )


def test_valid_txt():
    validator.is_valid_txt("this is sample text")

    with pytest.raises(Exception):
        validator.is_valid_txt("®€")
    with pytest.raises(Exception):
        validator.is_valid_txt("€")


def test_valid_srv():
    validator.is_valid_srv("0 5 5060 one.example.com.")

    with pytest.raises(Exception):
        validator.is_valid_srv("0 5 one.example.com.")
    with pytest.raises(Exception):
        validator.is_valid_srv("0 one.example.com.")
    with pytest.raises(Exception):
        validator.is_valid_srv("0 5 notanumber one.example.com.")
    with pytest.raises(Exception):
        validator.is_valid_srv("0 5 one.example.com.")


def test_valid_owner():
    validator.is_valid_owner("@")
    validator.is_valid_owner("*")
    validator.is_valid_owner("n")
    validator.is_valid_owner("ns")
    validator.is_valid_owner("a.b.c")
    validator.is_valid_owner("ns-ns-1")
    validator.is_valid_owner("ns1_")
    validator.is_valid_owner("_ns1_")
    validator.is_valid_owner(f"ns.ns.ns.{'a' * 63}")
    validator.is_valid_owner("a" * 255)

    with pytest.raises(Exception):
        validator.is_valid_owner("ns.")
    with pytest.raises(Exception):
        validator.is_valid_owner("ns-")
    with pytest.raises(Exception):
        validator.is_valid_owner("-ns")
    with pytest.raises(Exception):
        validator.is_valid_owner("ns.-ns.ns")
    with pytest.raises(Exception):
        validator.is_valid_owner("ns.ns-.ns")
    with pytest.raises(Exception):
        validator.is_valid_owner("ns()ns")
    with pytest.raises(Exception):
        validator.is_valid_owner("ns(ns")
    with pytest.raises(Exception):
        validator.is_valid_owner("ns)ns")
    with pytest.raises(Exception):
        # label more than 64
        validator.is_valid_owner(f"ns.ns.ns.{'a' * 64}")
    with pytest.raises(Exception):
        # owner more than 255
        validator.is_valid_owner("a" * 256)


def test_validate_func():
    # validator exists
    validator.validate("A", "192.0.2.1")

    with pytest.raises(Exception):
        # empty rdata
        validator.validate("TXT", "")

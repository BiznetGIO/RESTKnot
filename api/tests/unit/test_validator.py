import pytest

from app.helpers import validator


def test_valid_ip():
    validator.is_valid_ip("2001:db8:10::2")
    validator.is_valid_ip("192.0.2.1")

    with pytest.raises(Exception):
        validator.is_valid_ip("2001:db8:10::2::")
    with pytest.raises(Exception):
        validator.is_valid_ip("192.0.2")


def test_valid_mx():
    validator.is_valid_mx("10 mail.example.com.")
    validator.is_valid_mx("20 mail2.example.com")

    with pytest.raises(Exception):
        validator.is_valid_mx("mail.example.com.")
    with pytest.raises(Exception):
        validator.is_valid_mx("mail2.example.com")


def test_valid_cname():
    validator.is_valid_cname("example.com.")
    validator.is_valid_cname("example.com")

    with pytest.raises(Exception):
        validator.is_valid_cname("--example.com.")
    with pytest.raises(Exception):
        validator.is_valid_cname(".example.")


def test_valid_zone():
    validator.is_valid_zone("example.com")
    validator.is_valid_zone("foo.example.com")

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


def test_valid_owner():
    validator.is_valid_owner("@")
    validator.is_valid_owner("ns")
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
        # label more than 64
        validator.is_valid_owner(f"ns.ns.ns.{'a' * 64}")
    with pytest.raises(Exception):
        # owner more than 255
        validator.is_valid_owner("a" * 256)


def test_validate_func():
    # validator exists
    validator.validate("A", "192.0.2.1")
    # validator not exists
    validator.validate("SRV", "dummy")

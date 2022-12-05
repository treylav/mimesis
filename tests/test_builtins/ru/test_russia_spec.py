import pytest
from mimesis.builtins import RussiaSpecProvider
from mimesis.enums import Gender
from mimesis.exceptions import NonEnumerableError


@pytest.fixture
def russia():
    return RussiaSpecProvider()


@pytest.mark.parametrize(
    "first_issue, last_issue, result",
    [
        (1988, 1990, [88, 89, 90]),
        (1999, 2001, [99, 0, 1]),
        (1788, 1788, [88]),
        (99, 2022, list(range(0, 100))),
    ],
)
def test_possible_years_of_issue(russia, first_issue, last_issue, result):
    assert russia._get_possible_years_of_issue(first_issue, last_issue) == result


def test_invalid_possible_years_of_issue(russia):
    with pytest.raises(ValueError):
        russia._get_possible_years_of_issue(1818, 1817)


def test_passport_series(russia):
    series = russia.passport_series()
    assert isinstance(series.split(" "), list)


def test_passport_series_parametrized(russia):
    series = russia.passport_series(year=10)
    region, year = series.split(" ")
    assert int(year) == 10
    assert 0 < int(region) < 100


def test_passport_number(russia):
    result = russia.passport_number()
    assert isinstance(result, int)
    assert (result <= 999999) and (result >= 100000)


def test_series_and_number(russia):
    result = russia.series_and_number()
    assert result is not None


@pytest.mark.parametrize(
    "gender",
    [
        Gender.FEMALE,
        Gender.MALE,
    ],
)
def test_patronymic(russia, gender):
    result = russia.patronymic(gender=gender)

    assert result is not None
    assert len(result) >= 4

    with pytest.raises(NonEnumerableError):
        russia.patronymic(gender="nil")


def test_generate_sentence(russia):
    result = russia.generate_sentence()
    assert len(result) >= 20
    assert isinstance(result, str)


def test_snils(russia):
    result = russia.snils()
    assert len(result) == 11


def test_inn(russia):
    result = russia.inn()
    assert isinstance(result, str)
    assert result is not None


def test_ogrn_length(russia):
    result = russia.ogrn()
    assert len(result) == 13


@pytest.mark.parametrize(
    "sample, result",
    [
        ("103770001302", "0"),  # Bank Of Russia
        ("102770007051", "8"),  # Gazprom
        ("102770013219", "5"),  # Sberbank
        ("102773985096", "2"),  # VK
        ("102770022919", "3"),  # Yandex
    ],
)
def test_ogrn_control_digit(russia, sample, result):
    assert russia._generate_control_ogrn_digit(sample) == result


def test_ogrnip_control_digit(russia):
    assert (
        russia._generate_control_orgnip_digit("31453313670018") == "6"
    )  # Personal ORGNIP of committer


def test_ornip_length(russia):
    result = russia.ogrnip()
    assert len(result) == 15


def test_bic(russia):
    result = russia.bic()
    assert len(result) == 9


def test_kpp(russia):
    result = russia.kpp()
    assert len(result) == 9

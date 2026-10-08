from src.utils import eleva_quadrado, required_role
from unittest.mock import Mock, patch
import pytest
from http import HTTPStatus

@pytest.mark.parametrize("input, expected", [(4, 16), (8, 64)])
def test_eleva_quadrado(input, expected):
    resultado = eleva_quadrado(input)
    assert resultado == expected


@pytest.mark.parametrize(
    "input, type_exception, message",
    [
        ("a", TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
        (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")
    ]
)
def test_eleva_quadrado_negativo(input, type_exception, message):
    with pytest.raises(type_exception) as exeption:
        eleva_quadrado(input)
    assert str(exeption.value) == message


def test_required_role_sucess(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = required_role("admin")(lambda: "success")
    result = decorated_function()

    assert result == "success"


def test_required_role_fail(mocker):
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"
    
    mocker.patch('src.utils.get_jwt_identity')
    mocker.patch('src.utils.db.get_or_404', return_value=mock_user)
    decorated_function = required_role("admin")(lambda: "success")

    result = decorated_function()

    assert result == ({"message": "User don't have acess."}, HTTPStatus.FORBIDDEN)

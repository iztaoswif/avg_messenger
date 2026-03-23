from httpx import AsyncClient
import app.auth.exceptions as auth_exc

async def register(
    client: AsyncClient,
    username: str = "testuser",
    password: str = "password"):

    return await client.post("/auth/register", json={
        "username": username,
        "password": password
    })


async def login(
    client: AsyncClient,
    username: str = "testuser",
    password: str = "password"):

    return await client.post("/auth/login", data={
        "username": username,
        "password": password
    })


def assert_exception_response(
    response,
    predicted_exc: auth_exc.AuthException) -> None:

    assert response.status_code == predicted_exc.status_code
    assert response.json()["detail"] == predicted_exc.detail


def assert_successful_response(
    response,
    message = None) -> None:

    assert response.status_code == 200
    if message is not None:
        assert response.json()["message"] == message


#---------------------


async def test_register_success_basic(client: AsyncClient):
    response = await register(client)
    assert_successful_response(response, "Successful register")


async def test_register_success_multiple_users(client: AsyncClient):
    response1 = await register(client, "user1")
    assert_successful_response(response1, "Successful register")

    response2 = await register(client, "user2")
    assert_successful_response(response2, "Successful register")

    response3 = await register(client, "user3")
    assert_successful_response(response3, "Successful register")


async def test_register_fail_duplicate_username(client: AsyncClient):
    await register(client)
    response = await register(client)
    assert_exception_response(response, auth_exc.UsernameTakenError)


#-------------------------------
#login related tests


async def test_login_success_basic(client: AsyncClient):
    await register(client)
    response = await login(client)

    assert_successful_response(response)


async def test_login_fail_no_register(client: AsyncClient):
    response = await login(client)
    assert_exception_response(response, auth_exc.InvalidCredentialsError)


async def test_login_fail_invalid_password(client: AsyncClient):
    await register(client)

    response = await login(client, "testuser", "PasWoRDD")
    assert_exception_response(response, auth_exc.InvalidCredentialsError)

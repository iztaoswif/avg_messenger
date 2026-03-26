from httpx import AsyncClient


async def register_and_login(
    client: AsyncClient,
    username: str = "testuser") -> str:
    await client.post("/auth/register", json={
        "username": username,
        "password": "password"
    })

    response = await client.post("/auth/login",data={
        "username": username,
        "password": "password"
    })

    return response.json()["access_token"]


async def create_chat(
    client: AsyncClient,
    token: str,
    name: str = "testchat"):

    return await client.post("/chat/create",
        json={"name": name},
        headers={"Authorization": f"Bearer {token}"}
    )


async def send_message(
    client: AsyncClient,
    token: str,
    chat_id: int,
    content: str = "hello"):

    return await client.post("/chat/send",
        json={"chat_id": chat_id, "content": content},
        headers={"Authorization": f"Bearer {token}"}
    )


async def get_messages(
    client: AsyncClient,
    token: str,
    chat_id: int,
    after_id: int = 0):

    return await client.get(f"/chat/messages?chat_id={chat_id}&after_id={after_id}",
        headers={"Authorization": f"Bearer {token}"}
    )


def assert_exception_response(response, predicted_exc) -> None:
    assert response.status_code == predicted_exc.status_code
    assert response.json()["detail"] == predicted_exc.detail


def assert_successful_response(response, message=None) -> None:
    assert response.status_code == 200
    if message is not None:
        assert response.json()["message"] == message


#---------------------


async def test_create_chat_success(client: AsyncClient):
    token = await register_and_login(client)
    response = await create_chat(client, token)
    assert_successful_response(response)


async def test_creator_in_the_created_chat(
    client: AsyncClient,
    sqlite_connection):

    token = await register_and_login(client)
    await create_chat(client, token)

    exec_result = await sqlite_connection.execute("SELECT * FROM chat_members WHERE chat_id = 2")
    row = await exec_result.fetchone()

    assert row is not None
    assert row["user_id"] == 1

    assert await exec_result.fetchone() is None


async def test_create_chat_appears_in_list(client: AsyncClient):
    token = await register_and_login(client)
    await create_chat(client, token)

    response = await client.get("/chat/list",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert_successful_response(response)

    chats = response.json()["chats"]

    assert isinstance(chats, list)
    assert len(chats) == 2
    assert chats[1]["name"] == "testchat"


async def test_send_message_success(client: AsyncClient):
    token = await register_and_login(client)
    chat_response = await create_chat(client, token)
    chat_id = chat_response.json()["id"]

    response = await send_message(client, token, chat_id)
    assert_successful_response(response)


async def test_get_messages(client: AsyncClient):
    token = await register_and_login(client)
    chat_response = await create_chat(client, token)
    chat_id = chat_response.json()["id"]

    await send_message(client, token, chat_id, "hello")
    await send_message(client, token, chat_id, "world")

    response = await get_messages(client, token, chat_id)
    assert_successful_response(response)
    messages = response.json()["messages"]
    assert len(messages) == 2
    assert messages[0]["content"] == "hello"
    assert messages[1]["content"] == "world"


'''
async def test_join_chat(
    client: AsyncClient,
    sqlite_connection):

    token1 = await register_and_login(client, "user1")
    await create_chat(client, token1)

    token2 = await register_and_login(client, "user2")

    response = await client.post("/chat/join",
        json={"chat_id": 2},
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert_successful_response(response)

    exec_result = await sqlite_connection.execute("SELECT * FROM chat_members WHERE chat_id = 2")
    temp = 0

    row1 = await exec_result.fetchone()
    assert row1 is not None
    assert row1["user_id"] in (1, 2)

    temp += row1["user_id"]

    row2 = await exec_result.fetchone()
    assert row2 is not None
    assert row2["user_id"] in (1, 2)

    temp += row2["user_id"]

    assert temp == 3
    assert await exec_result.fetchone() is None
'''
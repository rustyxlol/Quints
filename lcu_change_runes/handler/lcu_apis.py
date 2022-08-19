async def LCU_GET(connection, endpoint):
    request = await connection.request("GET", endpoint)
    status_code = request.status

    if not request.ok:
        return status_code, None

    response = await request.json()
    return status_code, response


async def LCU_POST(connection, endpoint, payload):
    request = await connection.request("POST", endpoint, data=payload)
    status_code = request.status
    return status_code


async def LCU_DELETE(connection, endpoint):
    request = await connection.request("DELETE", endpoint)
    status_code = request.status
    return status_code

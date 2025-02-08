from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_header(x_line_signature: Annotated[str, Header()]):
    if not x_line_signature:
        raise HTTPException(status_code=400, detail="X-Line-Signature header is required")
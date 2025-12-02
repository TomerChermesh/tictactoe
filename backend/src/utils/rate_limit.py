from collections import deque
from time import monotonic
from typing import Deque, Dict

from fastapi import Request, HTTPException, status

from src.constants.fastapi import RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS



_requests_log: Dict[str, Deque[float]] = {}


async def rate_limiter(request: Request) -> None:
  client_ip: str = request.client.host if request.client else 'unknown'
  key: str = f'{client_ip}:{request.url.path}'
  now: float = monotonic()

  bucket: Deque[float] = _requests_log.setdefault(key, deque())

  while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
    bucket.popleft()

  if len(bucket) >= RATE_LIMIT_MAX_REQUESTS:
    raise HTTPException(
      status_code=status.HTTP_429_TOO_MANY_REQUESTS,
      detail='Too many requests, please slow down.'
    )

  bucket.append(now)



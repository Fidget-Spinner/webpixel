"""
Unit tests for various small but critical operations.
"""

from unittest import mock

import asyncio
import aiofiles


async def test_aiofile_write():
    """ testing asyncio file write """
    aiofiles.threadpool.wrap.register(mock.MagicMock)(
        lambda *args, **kwargs: aiofiles.threadpool.AsyncBufferedIOBase(*args, **kwargs))
    data = 'data'
    mock_file = mock.MagicMock()

    with mock.patch('aiofiles.threadpool.sync_open', return_value=mock_file) as mock_open:
        async with aiofiles.open('filename', 'w') as f:
            await f.write(data)
        mock_file.write.assert_called_once_with(data)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(test_aiofile_write())

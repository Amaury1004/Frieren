import aiohttp
import io

class CatsNetwork:
    def __init__(self, api_key: str):
        self.api_url = "https://api.thecatapi.com/v1/images/search?limit=1"
        self.headers = {
            "x-api-key": api_key
        }

    async def fetch_image(self) -> io.BytesIO:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            # 1️⃣ Получаем JSON
            async with session.get(self.api_url) as response:
                data = await response.json()

                # TheCatAPI возвращает массив
                image_url = data[0]["url"]

            # 2️⃣ Загружаем картинку
            async with session.get(image_url) as image_response:
                image_bytes = await image_response.read()

        return io.BytesIO(image_bytes)

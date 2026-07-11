import requests
import time


request_count = 0


def api_get(url):

    global request_count

    retry = 0

    while True:

        try:

            response = requests.get(
                url,
                timeout=10
            )


            if response.status_code == 429:

                if retry < 2:

                    retry += 1

                    print(
                        "⚠️ Rate limit - waiting 15 seconds..."
                    )

                    time.sleep(15)

                    continue

                else:

                    print(
                        "❌ Request skipped"
                    )

                    return None



            if response.status_code != 200:

                print(
                    "API Error:",
                    response.status_code
                )

                return None



            request_count += 1


            if request_count >= 3:

                print(
                    "⏳ API cooldown 3 seconds..."
                )

                time.sleep(3)

                request_count = 0



            return response.json()



        except Exception as e:

            print(
                "Connection error:",
                e
            )

            return None
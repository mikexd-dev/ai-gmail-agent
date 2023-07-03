import requests

print(
    requests.post(
        "http://0.0.0.0:10000",
        headers={
            'Content-Type': 'application/json'
        },
        json={
            "from_email": "asdasd@gmail.com",
            "content": """
                Dear Jason 
                I hope this message finds you well. I'm Shirley from Gucci;

                I'm looking to purchase some company T-shirt for my team, we are a team of 100k people, and we want to get 2 t-shirt per personl

                Please let me know the price and timeline you can work with;

                Looking forward

                Shirley Lou
            """
        }
    ).json()
)

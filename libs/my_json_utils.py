class MyJsonUtils:

    def content_data_store(self):
        data = {
            1: {
                "title": "Sauce Labs Backpack",
                "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
                "price": "$29.99"
            },
            2: {
                "title": "Sauce Labs Bike Light",
                "description": "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
                "price": "$9.99"
            },
            3: {
                "title": "Sauce Labs Bolt T-Shirt",
                "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
                "price": "$15.99"
            },
            4: {
                "title": "Sauce Labs Fleece Jacket",
                "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
                "price": "$49.99"
            },
            5: {
                "title": "Sauce Labs Onesie",
                "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
                "price": "$7.99"
            },
            6: {
                "title": "Test.allTheThings() T-Shirt (Red)",
                "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
                "price": "$15.99"
            }
        }
        return data


class MyApiJsonUtils:

    def pets_endpoints_info(self, **kwargs):
        data = {
            "pet": {
                "method": {
                    'create': "POST",
                    'edit': "PUT"
                },
                "url": "/pet",

                },
            "pet_id": {
                "method": {
                    "read": "GET",
                    "delete": "DELETE"
                },
                "url": f"/pet/{kwargs['id'] if 'id' in kwargs else ''}",
            }
        }
        return data

    def generate_body_pet(self, **kwargs):
        body = {
                  "id": 0,
                  "category": {
                        "id": 0,
                        "name": f"{kwargs['category_name'] if 'category_name' in kwargs else ''}"
                    },
                  "name": f"{kwargs['pet_type'] if 'pet_type' in kwargs else ''}",
                  "photoUrls": [
                        "string"
                      ],
                  "tags": [
                        {
                          "id": 0,
                          "name": f"{kwargs['tag_name'] if 'tag_name' in kwargs else ''}"
                        }
                  ],
                  "status": f"{kwargs['status'] if 'status' in kwargs else 'available'}"
                }
        return body



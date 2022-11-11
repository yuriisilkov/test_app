import logging
from libs.my_json_utils import MyApiJsonUtils
import requests
from libs.my_decorators import description


logger = logging.getLogger("My_logs")


class MyAPI():

    def __init__(self):
        self.base_url = "https://petstore.swagger.io/v2"
        self.api_json_utils = MyApiJsonUtils()
        self.pet_id = None

    def send_request(self, method, url, payload=None, headers=None, auth=None, json=None, negative=None):
        try:
            response = requests.request(method, url, headers=headers, auth=auth, json=json, data=payload)
        except Exception as exc:
            logger.error(f"Request failed due to: {exc}")
            return False
        if negative:
            if response.status_code == 200:
                logger.error(f"{method} {url}: returned status code: {response.status_code}")
                return False
            else:
                logger.info(f"{method} {url}: returned status code: '{response.status_code}' as expected")
                return True
        if response.status_code != 200:
            logger.error(f"{method} {url}: returned status code: {response.status_code}")
            logger.error(f"Text message: {response.text}")
            return False
        logger.info(f"{method} {url}: returned status code: '{response.status_code}'")
        return response

    def verify_response(self, response, **kwargs):
        res = response.json()
        if 'category_name' in kwargs:
            if not res['category']['name'] == kwargs['category_name']:
                logger.error(f"Expected response category name: '{kwargs['category_name']}' not equal with actual: '{res['category']['name']}'")
                return False

        if 'pet_type' in kwargs:
            if not res['name'] == kwargs['pet_type']:
                logger.error(
                    f"Expected response name: '{kwargs['pet_type']}' not equal with actual: '{res['name']}'")
                return False
        if 'tag_name' in kwargs:
            for tag in res['tags']:
                if not tag['name'] == kwargs['tag_name']:
                    logger.error(
                        f"Expected response tag name: '{kwargs['tag_name']}' not equal with actual: '{res['tag']['name']}'")
                    return False
        if 'status' in kwargs:
            if not res['status'] == kwargs['status']:
                logger.error(
                    f"Expected response status: '{kwargs['status']}' not equal with actual: '{res['status']}'")
                return False
        logger.info('Response verification successfully passed')
        return True

    @description("Function name: 'Post on pet'")
    def post_on_pet(self):
        pets_info = self.api_json_utils.pets_endpoints_info()
        url = f"{self.base_url}{pets_info['pet']['url']}"
        method = pets_info['pet']['method']['create']
        body = self.api_json_utils.generate_body_pet(category_name='food', pet_type='dog',
                                                     tag_name='Ukraine')
        response = self.send_request(method, url, json=body)
        if not response:
            return False
        if not self.verify_response(response, category_name='food', pet_type='dog', tag_name='Ukraine'):
            return False
        self.pet_id = response.json()['id']
        return True

    @description("Function name: 'Get on pet by id'")
    def get_on_pet_by_id(self):
        pets_info = self.api_json_utils.pets_endpoints_info(id=self.pet_id)
        url = f"{self.base_url}{pets_info['pet_id']['url']}"
        method = pets_info['pet_id']['method']['read']
        response = self.send_request(method, url)
        if not response:
            return False
        if not self.verify_response(response, category_name='food', pet_type='dog', tag_name='Ukraine', status='available'):
            return False
        return True

    @description("Function name: 'Put on pet'")
    def put_on_pet(self):
        pets_info = self.api_json_utils.pets_endpoints_info()
        url = f"{self.base_url}{pets_info['pet']['url']}"
        method = pets_info['pet']['method']['edit']
        body = self.api_json_utils.generate_body_pet(category_name='food', pet_type='dog',
                                                     tag_name='Ukraine', status='sold')
        response = self.send_request(method, url, json=body)
        if not response:
            return False
        if not self.verify_response(response, category_name='food', pet_type='dog', tag_name='Ukraine', status='sold'):
            return False
        return True

    @description("Function name: 'Delete pet'")
    def delete_pet(self):
        pets_info = self.api_json_utils.pets_endpoints_info(id=self.pet_id)
        url = f"{self.base_url}{pets_info['pet_id']['url']}"
        method = pets_info['pet_id']['method']['delete']
        response = self.send_request(method, url)
        if not response:
            return False
        logger.info("Verify object after deletion..")
        method = pets_info['pet_id']['method']['read']
        response = self.send_request(method, url, negative=404)
        if not response:
            return False
        return True



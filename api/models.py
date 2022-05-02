import json


class User:
    id = 0
    first_name = ""
    last_name = ""
    phone_number = ""
    email = ""
    company_name = ""
    profiles = []
    settings = None

    def __init__(self, id, first_name, last_name, phone_number, email, company_name, profiles, settings):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.company_name = company_name
        self.profiles = profiles
        self.settings = settings

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Profile:
    id = 0
    name = ""
    attributes = []

    def __init__(self, id, name, attributes):
        self.id = id
        self.name = name
        self.attributes = attributes

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Settings:
    id = 0
    phone_number_visibility = False
    company_name_visibility = False
    directory_visibility = False

    def __init__(self, id, phone_number_visibility, company_name_visibility, directory_visibility):
        self.id = id
        self.phone_number_visibility = phone_number_visibility
        self.company_name_visibility = company_name_visibility
        self.directory_visibility = directory_visibility

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

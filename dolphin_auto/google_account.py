import random
import string
import names


class GoogleAcc:
    def __init__(self):
        self.gender = 'male' if random.randrange(0, 2) else 'female'
        self.firstName = names.get_first_name(gender=self.gender)
        self.lastName = names.get_last_name()
        self.bornDay = random.randrange(1, 31)
        self.bornMonth = random.randrange(1, 13)
        self.bornYear = random.randrange(1990, 2004)
        self.username = self.lastName + self.firstName + str(random.randrange(100, 1000)) + ''.join(
            random.choice(string.ascii_uppercase) for i in range(2))
        chars = string.ascii_letters + string.digits + string.punctuation
        self.password = ''.join(random.choice(chars) for i in range(12))

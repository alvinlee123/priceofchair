import uuid
from src.common.database import Database
import src.models.users.errors as UserErrors
from src.common.utils import Utils

class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id



    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email,password):
        """

        This method verifies that an email/password combo (as sent by the site forms) is
        valid or not. Check that the email exists and that the password associated with
        that email is correct

        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one("users", {"email": email}) # password in sha512 ->pbkdf2_sha512
        if user_data is None:
            #tell that the user that their email doesn't exist
            raise UserErrors.UserNotExistsError("Your User does not exist")

        if not Utils.check_hashed_password(password, user_data['password']):
            #tell user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong.")

        return True

    @staticmethod
    def register_user(email,password):
        """
        This method registers a user using e-mail and password
        Password will come hashed as sha-512
        :param email: user's email (may be invalid)
        :param password:  sha-512 hashed password
        :return: true if registered successful, False otherwise (exceptions can also be raised_
        """
        user_data = Database.find_one("users", {"email":email})

        if user_data is not None:
            # Tell user they are already registered
            raise UserErrors.UserAlreadyRegistered("The e-mail you used to register already exists")
        if not Utils.email_is_valid(email):
            # tell user email not constructed properly
            raise UserErrors.InvalidEmailError("The e-mail you used does not have the right format")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users",self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password":self.password
        }
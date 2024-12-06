from flask_login import UserMixin
from flask_principal import Permission, RoleNeed

admin_permission = Permission(RoleNeed("admin"))
user_permission = Permission(RoleNeed("user"))

class Usuario(UserMixin):
    def __init__(self, id, cargo):
        self.id = id
        self.cargo = cargo

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, value):
        self._cargo = value

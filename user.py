class Current_user:
	logged_in = False
	username = None
	email = None
	id = None

	def is_login(self):
		return self.logged_in

	def login(self):
		self.logged_in = True

	def logout(self):
		self.username = None
		self.email = None
		self.id = None
		self.logged_in = False
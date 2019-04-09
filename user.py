class Current_user:
	logged_in = False
	username = None
	email = None

	def is_login(self):
		return self.logged_in

	def login(self):
		self.logged_in = True

	def logout(self):
		username = None
		email = None
		self.logged_in = False
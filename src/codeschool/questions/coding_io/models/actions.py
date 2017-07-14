from django.utils.html import escape

class Actions:
	def regrade_post(self):
		"""
        Regrade all submissions using the post tests.
        """

		self.responses.regrade_with(self.post_tests_expanded)

	def action_expand_tests(self, client, *args, **kwargs):
		self._expand_tests()
		pre = escape(self.pre_tests_expanded_source)
		post = escape(self.post_tests_expanded_source)
		client.dialog('<h2>Pre-tests</h2><pre>%s</pre>'
					  '<h2>Post-test</h2><pre>%s</pre>' % (pre, post))

	def action_grade_with_post_tests(self, client, *args, **kwargs):
		self.regrade_post()
		client.dialog('<p>Successful operation!</p>')
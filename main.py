import os
import webapp2
import jinja2
import cgi
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = False)

def esc_html(s):
    """
    Returns user input as an escaped string
    """
    return cgi.escape(s, quote=True)


class Handler(webapp2.RequestHandler):
    # Handler that renders jinja2 templates

	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


def str_match_roman(s):
    """ 
    Checks string for letters that are Roman Numerals. 
    Returns False if string contains foreign characters.
    """
    reg = re.compile(r"^[ivxlcdmIVXLCDM]+$")
    return reg.match(s)

def sub_principle(numbers):
    """
    Subtractive Principle 
    
    If a smaller number occurs before a larger number, the former is subtracted.
    - e.g.(XC ==> C - X ==> 100 - 10 = 90)
    """
    result = 0
    for index in xrange(len(numbers) - 1):
        if numbers[index] < numbers[index + 1]:
            numbers[index + 1] -= numbers[index]
            numbers[index] = 0
    for num in numbers:
        result += num
    return result

def numeral_to_num(numerals):
    """
    Converts Roman Numerals to a number.
    """
    converters = {'I': 1, 'i': 1, 'V': 5, 'v': 5, 
                 'X': 10, 'x': 10, 'L': 50, 'l': 50, 
                 'C': 100, 'c': 100, 'D': 500, 'd': 500,
                 'M': 1000, 'm': 1000}
    numbers = []
    for numeral in numerals:
        for key in converters:
            if numeral == key:
                numbers.append(converters[key])
    return sub_principle(numbers)
	
def valid_roman(numerals):
	"""
	Checks string for valid Roman Numerals syntax.
	"""
	pass
	

class Main(Handler):
    """
    Main handler that renders the html page, manages input from the form 
    and renders the appropriate output.
    """
    def write_page(self, user_input="", output=""):
        self.render('index.html', user_input=user_input, output=output)

    def get(self):
        self.write_page()

    def post(self):
        user_input = esc_html(self.request.get('user_input'))
        number = ''

        # user input must be a string that contains Roman Numeral letters
        if user_input.isdigit() or not (str_match_roman(user_input)):
            error = "<span style='color:red;'>Input must be in Roman Numerals.</span>"
            self.write_page(user_input=user_input, output=error)

        else:
            number = numeral_to_num(user_input)
            self.write_page(user_input=user_input, output=number)

app = webapp2.WSGIApplication([('/', Main)], debug=True)

import os
import webapp2
import jinja2
import cgi
import re
from collections import Counter

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = False)

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
    Converts Roman Numerals to a list of numbers.
    """
    converters = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 
                 'C': 100, 'D': 500, 'M': 1000}
    numbers = []
    for numeral in numerals:
        for key in converters:
            if numeral == key:
                numbers.append(converters[key])
    return numbers
	
def power_of_ten(num):
    return num == 1 or num % 10 == 0

def valid_roman(numerals):
    """
    Checks string for valid Roman Numerals syntax.
    """
    numbers = numeral_to_num(numerals)
    for index in xrange(len(numbers) - 1):
        nextNum = numbers[index + 1]
        if numbers[index] == nextNum:
            return True
        elif numbers[index] * 10 >= nextNum:
            if power_of_ten(numbers[index]):
                return True

def repetition_rule(numerals):
    """
    Checks for a Numeral that repeats consecutively four times or more.
    """
    freq = []
    for index in xrange(len(numerals) - 1):
        if numerals[index] == numerals[index + 1]:
            if freq:
                freq.append(numerals[index])
            else:
                freq.append(numerals[index])
                freq.append(numerals[index + 1])
    return len(freq) >= 4

class Main(Handler):
    """
    Main handler that renders the html page, manages input from the form 
    and renders the appropriate output.
    """
    def write_page(self, output=""):
        self.render('index.html', output=output)

    def get(self):
        self.write_page()

    def post(self):
		# input is escaped and converted into uppercase
        user_input = esc_html(self.request.get('user_input')).upper()

	    # user input must be a string that contains Roman Numeral letters
        if user_input.isdigit() or not (str_match_roman(user_input)):
            output = "<span style='color:red;'>Input must be in Roman Numerals.</span>"

        # user input must follow proper syntax
        elif not valid_roman(user_input):
            output = """<span style='color:red;'>Your syntax is off. Follow these rules:</span><br>
                       <span style='color:red;'>Only I can go before V or X,</span><br>
                       <span style='color:red;'>X before L or C,</span><br>
                       <span style='color:red;'>C before D or M.</span>"""
            output += "<br><br>" + user_input

        # numbers equal to 3999 and up require a special character and can't be handled
        elif sub_principle(numeral_to_num(user_input)) >= 4000:
            output = """<span style='color:red;'>Sorry. Can't handle numbers 4000 or greater.</span><br>
                        <a href='http://able2know.org/topic/54469-1'>Here's why</span>"""

        # user input cannot have a Roman Numeral that repeats four times or more in a row
        elif repetition_rule(user_input):
            output = "<span style='color:red;'>Is your key stuck?</span>"

        else:
            numList = numeral_to_num(user_input)
            output = "{0} --> {1}" .format(user_input, sub_principle(numList))
        
        self.write_page(output=output)

app = webapp2.WSGIApplication([('/', Main)], debug=True)

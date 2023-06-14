from code_feedback import Feedback
from pl_helpers import name, points
from pl_unit_test import PLTestCase
import random as rd
import inspect

class Test(PLTestCase):
    total_iters = 5
    def setUp(self):
        self.output = eval("self.st." + self.data["params"]["fname"])
        
        def test_function_args(func):
            argspec = inspect.getfullargspec(func)
            args = argspec.args
            varargs = argspec.varargs
            keywords = argspec.varkw
            if varargs or keywords:
                raise TypeError(f"{func.__name__}() accepts *args or **kwargs")
            if len(args) != 1:
                raise TypeError(f"{func.__name__}() takes 1 positional arguments, but {len(args)} were given")
        self.test_function_args = test_function_args
    
    @points(1/total_iters)
    @name("correct input parameters (only 1 parameter, no *args or **kwargs)")
    def test_0(self):
        try:
            self.test_function_args(self.output)
            Feedback.set_score(1)
        except:
            Feedback.set_score(0)
        
    @points(1)
    @name("random input")
    def test_1(self):
                               #(feedback var name, ans.py variable, student answer variable)
        randint = rd.randint(10, 1000)
        feedback = str(self.data["params"]["fname"]) + "(" + str(randint) + ") = " + str(self.output(randint))
        if Feedback.check_scalar(feedback, self.ref.correct_output(randint), self.output(randint)):
            Feedback.set_score(1)

        else:
            Feedback.set_score(0)
    
    @points(2/total_iters)
    @name("edge case #1")
    def test_2(self):
        input_num = 0
        feedback = str(self.data["params"]["fname"]) + "(" + str(input_num) + ") = " + str(self.output(input_num))
        if Feedback.check_scalar(feedback, self.ref.correct_output(input_num), self.output(input_num)):
            Feedback.set_score(1)

        else:
            Feedback.set_score(0)
    
    @points(2/total_iters)
    @name("edge case #2")
    def test_3(self):
        input_num = 1
        feedback = str(self.data["params"]["fname"]) + "(" + str(input_num) + ") = " + str(self.output(input_num))
        if Feedback.check_scalar(feedback, self.ref.correct_output(input_num), self.output(input_num)):
            Feedback.set_score(1)

        else:
            Feedback.set_score(0)
import unittest
from app.models import Pitch, User, Comment
from app import db

class TestPitch(unittest.TestCase):

    def setUp(self):
        self.new_grematter = Greymatter(greymatter_content = "blog post",)
        self.new_comment = Comment(comment_content = "comment", pitch=self.new_pitch)
    
    def tearDown(self):
        db.session.delete(self)
        User.query.commit()
        

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment_content,"comment")
        self.assertEquals(self.new_comment.pitch,self.new_pitch, 'pitcher')

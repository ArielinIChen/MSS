# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.


class Test(object):
    def __init__(self, whoami):
        self.whoami = whoami

        if self.whoami == 'cat':
            self.cat()
        elif self.whoami == 'dog':
            self.dog()
        elif self.whoami == 'wolf':
            self.wolf()
        else:
            print 'not matched'

    def cat(self):
        return 'miao miao miao'

    def dog(self):
        return 'wang wang wang'

    def wolf(self):
        return 'Ao Wuuuuuu~'


Test('dog')
Test('cat')
Test('wolf')
Test('human')

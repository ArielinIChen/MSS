# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.hashers import PBKDF2PasswordHasher, SHA1PasswordHasher

# Create your tests here.


# class Test(object):
#     def __init__(self, whoami):
#         self.whoami = whoami
#
#         if self.whoami == 'cat':
#             self.cat()
#         elif self.whoami == 'dog':
#             self.dog()
#         elif self.whoami == 'wolf':
#             self.wolf()
#         else:
#             print 'not matched'
#
#     def cat(self):
#         return 'miao miao miao'
#
#     def dog(self):
#         return 'wang wang wang'
#
#     def wolf(self):
#         return 'Ao Wuuuuuu~'
#
#
# Test('dog')
# Test('cat')
# Test('wolf')
# Test('human')


# class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
#     algorithm = 'pbkdf2_wrapped_sha1'
#
#     def encode_sha1_hash(self, sha1_hash, salt, iterations=None):
#         return super().encode(sha1_hash, salt, iterations)
#
#     def encode(self, password, salt, iterations=None):
#         _, _, sha1_hash = SHA1PasswordHasher().encode(password, salt).split('$', 2)
#         return self.encode_sha1_hash(sha1_hash, salt, iterations)
#

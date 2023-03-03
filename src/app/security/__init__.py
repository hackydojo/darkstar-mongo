from abc import ABCMeta, abstractmethod


# -------------------------------------------------------------------------
# CLASS IDENTITY CREDENTIAL
# -------------------------------------------------------------------------
class IdentityCredential:
    __metaclass__ = ABCMeta

    @abstractmethod
    def verify(self, **kwargs):
        pass

from Box2D import *


def callOnBoth(contact: b2Contact, fName: str, *args):
    objA = contact.fixtureA.body.userData
    objB = contact.fixtureB.body.userData
    getattr(objA, fName)(objB, contact, *args)
    getattr(objB, fName)(objA, contact, *args)


class ContactListener(b2ContactListener):
    def BeginContact(self, contact: b2Contact):
        callOnBoth(contact, "beginContact")

    def EndContact(self, contact: b2Contact):
        callOnBoth(contact, "endContact")

    def PreSolve(self, contact: b2Contact, oldManifold: b2Manifold):
        callOnBoth(contact, "preSolve", oldManifold)

    def PostSolve(self, contact: b2Contact, impulse: b2ContactImpulse):
        callOnBoth(contact, "postSolve", impulse)

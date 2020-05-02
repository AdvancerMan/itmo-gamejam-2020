from Box2D import *

from objects.base.InGameObject import InGameObject


def callOnBoth(contact: b2Contact, f, *args):
    objA = contact.fixtureA.body.userData
    objB = contact.fixtureB.body.userData
    f(objA, objB, contact, *args)
    f(objB, objA, contact, *args)


class ContactListener(b2ContactListener):
    def BeginContact(self, contact: b2Contact):
        callOnBoth(contact, InGameObject.beginContact)

    def EndContact(self, contact: b2Contact):
        callOnBoth(contact, InGameObject.endContact)

    def PreSolve(self, contact: b2Contact, oldManifold: b2Manifold):
        callOnBoth(contact, InGameObject.preSolve, oldManifold)

    def PostSolve(self, contact: b2Contact, impulse: b2ContactImpulse):
        callOnBoth(contact, InGameObject.postSolve, impulse)

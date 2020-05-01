from Box2D import *
from objects.base import InGameObject


class BodyFactory:
    def __init__(self, world: b2World):
        self.__world = world

    def createBody(self, owner: InGameObject, bodyType: int, **kwargs) -> b2Body:
        """
        b2BodyType 	bodyType --- use b2_dynamicBody, b2_kinematicBody or b2_staticBody
        b2Vec2 	    position
        float 	    angle --- The world angle of the body in radians.
        b2Vec2 	    linearVelocity --- The linear velocity of the body's origin in world co-ordinates.
        float 	    angularVelocity --- The angular velocity of the body.
        float 	    linearDamping
        float 	    angularDamping
        bool 	    allowSleep
        bool 	    awake --- Is this body initially awake or sleeping?
        bool 	    fixedRotation --- Should this body be prevented from rotating? Useful for characters.
        bool 	    bullet
        bool 	    active --- Does this body start out active?
        void * 	    userData  --- Use this to store application specific body data.
        float 	    gravityScale  --- Scale the gravity applied to this body.
        copied from https://box2d.org/documentation/structb2_body_def.html

        CreateBody(..., fixtures=[])
        This is short for:
        body = CreateBody(...)
        for fixture in []:
            body.CreateFixture(fixture)

        CreateBody(..., shapes=[], shapeFixture=b2FixtureDef())
        This is short for:
            body = CreateBody(...)
            body.CreateFixturesFromShapes(shapes=[], shapeFixture=b2FixtureDef())
        copied from b2World.CreateBody.__doc__
        """
        return self.__world.CreateBody(userData=owner, type=bodyType, **kwargs)

    def createRectangleBody(self, owner: InGameObject, bodyType: int, width: int, height: int) -> b2Body:
        shape = b2PolygonShape()
        shape.SetAsBox(width, height)
        return self.createBody(owner, bodyType, fixtures=b2FixtureDef(shape=shape))

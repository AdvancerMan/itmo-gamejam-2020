from Box2D import *
from objects.main.InGameObject import toMeters


class BodyTemplate:
    def __init__(self, **kwargs):
        assert "bodyType" in kwargs.keys()
        self.__kwargs = kwargs

    def createBody(self, factory):
        # factory: BodyFactory
        # Note: after creating you should set body owner (use setUserData())
        return factory.createBody(**self.__kwargs)


def _getRectangleBodyInfo(bodyType: int, width: float, height: float, **kwargs) -> dict:
    shape = b2PolygonShape()
    shape.SetAsBox(toMeters(width) / 2, toMeters(height) / 2)
    kwargs.update({"bodyType": bodyType, "fixtures": b2FixtureDef(friction=0, shape=shape)})
    return kwargs


def _getCircleBodyInfo(bodyType: int, radius: float, **kwargs) -> dict:
    shape = b2CircleShape()
    shape.radius = toMeters(radius)
    kwargs.update({"bodyType": bodyType, "fixtures": b2FixtureDef(friction=0, shape=shape)})
    return kwargs


def createCircleBodyTemplate(bodyType: int, radius: float, **kwargs) -> BodyTemplate:
    return BodyTemplate(**_getRectangleBodyInfo(bodyType, radius, **kwargs))


def createRectangleBodyTemplate(bodyType: int, width: float, height: float, **kwargs) -> BodyTemplate:
    return BodyTemplate(**_getRectangleBodyInfo(bodyType, width, height, **kwargs))


class BodyFactory:
    def __init__(self, world: b2World):
        self.__world = world

    def createBody(self, bodyType: int, **kwargs) -> b2Body:
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
        return self.__world.CreateBody(type=bodyType, **kwargs)

    def createRectangleBody(self, bodyType: int, width: float, height: float, **kwargs) -> b2Body:
        return self.createBody(**_getRectangleBodyInfo(bodyType, width, height, **kwargs))

    def createCircleBody(self, bodyType: int, radius: float, **kwargs) -> b2Body:
        return self.createBody(**_getCircleBodyInfo(bodyType, radius, **kwargs))

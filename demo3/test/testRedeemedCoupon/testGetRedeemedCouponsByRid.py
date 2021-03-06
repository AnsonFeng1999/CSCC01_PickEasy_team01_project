import unittest
from models import Redeemed_Coupons, User, Coupon, Restaurant
from models import db
import time
import datetime
from app import app
from databaseHelpers import redeemedCoupons as rchelper

BEGIN = datetime.date(2020, 5, 1)
END = datetime.date(2020, 6, 30)


class SelectCustomerCoupons(unittest.TestCase):
    """
    Tests get_redeemed_coupons_by_rid() in databaseHelpers.redeemedCoupons.py.
    """
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_no_coupon(self):
        """
        Checks retrieving a list of no coupons.
        """
        redeemed_coupon_list = rchelper.get_redeemed_coupons_by_rid(20)
        self.assertEqual(redeemed_coupon_list, [])

    def test_one_coupon_one_user_valid(self):
        """
        Checks retrieving a list of one valid coupon belonging to one user. Expect output to match correct data.
        """
        restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
        db.session.add(restaurant)
        db.session.commit()
        coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", level=36, begin=BEGIN, expiration=END, deleted=0)
        user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
        db.session.add(coupon)
        db.session.commit()
        db.session.add(user)
        db.session.commit()
        redeemed_coupon = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, valid = 1)
        db.session.add(redeemed_coupon)
        db.session.commit()

        redeemed_coupon_list = rchelper.get_redeemed_coupons_by_rid(restaurant.rid)

        self.assertEqual(redeemed_coupon_list,[
            {
                "cid": coupon.cid,
                "name": "test",
                "description": "50% off",
                "points": 10,
                "level": 36,
                "begin": BEGIN,
                "expiration": END,
                "deleted": 0,
                "holders": 1,
                "used": 0

            }
        ])

    def test_one_coupon_one_user_invalid(self):
        """
        Checks retrieving a list of one invalid coupon belonging to one user. Expect output to match correct data.
        """
        restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
        db.session.add(restaurant)
        db.session.commit()
        coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", level=22, begin=BEGIN, expiration=END, deleted=0)
        user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
        db.session.add(coupon)
        db.session.commit()
        db.session.add(user)
        db.session.commit()
        redeemed_coupon = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, valid = 0)
        db.session.add(redeemed_coupon)
        db.session.commit()

        redeemed_coupon_list = rchelper.get_redeemed_coupons_by_rid(restaurant.rid)

        self.assertEqual(redeemed_coupon_list,[
            {
                "cid": coupon.cid,
                "name": "test",
                "description": "50% off",
                "points": 10,
                "level": 22,
                "begin": BEGIN,
                "expiration": END,
                "deleted": 0,
                "holders": 0,
                "used": 1

            }
        ])

    def test_one_coupon_no_user(self):
        """
        Checks retrieving a list of one valid coupon belonging to no users. Expect output to match correct data.
        """
        restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
        db.session.add(restaurant)
        db.session.commit()
        coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", level=55, begin=BEGIN, expiration=END, deleted=0)
        user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
        db.session.add(coupon)
        db.session.commit()
        db.session.add(user)
        db.session.commit()

        redeemed_coupon_list = rchelper.get_redeemed_coupons_by_rid(restaurant.rid)

        self.assertEqual(redeemed_coupon_list,[
            {
                "cid": coupon.cid,
                "name": "test",
                "description": "50% off",
                "points": 10,
                "level": 55,
                "begin": BEGIN,
                "expiration": END,
                "deleted": 0,
                "holders": 0,
                "used": 0
            }
        ])

    def test_one_coupon_many_customers(self):
        """
        Checks retrieving a list of one coupon belonging to many users. Expect output to match correct data.
        """
        restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
        db.session.add(restaurant)
        db.session.commit()
        coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", level=33, begin=BEGIN, expiration=END, deleted=0)
        user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
        user2 = User(uid = 6, name = "John", email = "John@gmail.com", password = "password", type = -1)
        db.session.add(coupon)
        db.session.commit()
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        redeemed_coupon1 = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, valid = 1)
        redeemed_coupon2 = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user2.uid, valid = 1)
        redeemed_coupon3 = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, valid = 0)
        db.session.add(redeemed_coupon1)
        db.session.add(redeemed_coupon2)
        db.session.add(redeemed_coupon3)
        db.session.commit()

        redeemed_coupon_list = rchelper.get_redeemed_coupons_by_rid(restaurant.rid)

        self.assertEqual(redeemed_coupon_list,[
            {
                "cid": coupon.cid,
                "name": "test",
                "description": "50% off",
                "points": 10,
                "level": 33,
                "begin": BEGIN,
                "expiration": END,
                "deleted": 0,
                "holders": 2,
                "used": 1
            }
        ])

    def test_many_coupons(self):
        """
        Checks retrieving a list of many coupons belonging to many users. Expect output to match correct data.
        """
        restaurant = Restaurant(name = "David's Restaurant", address = "1234 Main Street", uid = 17)
        db.session.add(restaurant)
        db.session.commit()
        coupon = Coupon(rid = restaurant.rid, name="test", points=10, description="50% off", level=1, begin=BEGIN, expiration=END, deleted=0)
        coupon2 = Coupon(rid = restaurant.rid, name="test2", points=10, description="25% off", level=2, begin=BEGIN, expiration=END, deleted=0)
        user = User(uid = 5, name = "Joe", email = "joe@gmail.com", password = "password", type = -1)
        user2 = User(uid = 6, name = "John", email = "John@gmail.com", password = "password", type = -1)
        db.session.add(coupon)
        db.session.add(coupon2)
        db.session.commit()
        db.session.add(user)
        db.session.add(user2)
        db.session.commit()
        redeemed_coupon1 = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, valid = 1)
        redeemed_coupon2 = Redeemed_Coupons(cid = coupon2.cid, rid = restaurant.rid, uid = user2.uid, valid = 1)
        redeemed_coupon3 = Redeemed_Coupons(cid = coupon.cid, rid = restaurant.rid, uid = user.uid, valid = 0)
        db.session.add(redeemed_coupon1)
        db.session.add(redeemed_coupon2)
        db.session.add(redeemed_coupon3)
        db.session.commit()

        redeemed_coupon_list = rchelper.get_redeemed_coupons_by_rid(restaurant.rid)

        self.assertEqual(redeemed_coupon_list,[
            {
                "cid": coupon.cid,
                "name": "test",
                "description": "50% off",
                "points": 10,
                "level": 1,
                "begin": BEGIN,
                "expiration": END,
                "deleted": 0,
                "holders": 1,
                "used": 1
            },
            {
                "cid": coupon2.cid,
                "name": "test2",
                "description": "25% off",
                "points": 10,
                "level": 2,
                "begin": BEGIN,
                "expiration": END,
                "deleted": 0,
                "holders": 1,
                "used": 0
            }
        ])

if __name__ == "__main__":
    unittest.main()

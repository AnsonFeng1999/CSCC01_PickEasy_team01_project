import unittest
from models import User, Coupon, Restaurant, Employee
from models import db
import datetime
from app import app
from databaseHelpers import coupon as couponhelper

BEGIN = datetime.date(2020, 5, 1)
END = datetime.date(2020, 6, 30)


class SingleSelectorCouponTest(unittest.TestCase):
    """
    Tests get_coupon_by_cid() in coupon.py.
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

    def test_coupon_no_matching(self):
        """
        Test getting no matching coupon, with a coupon in database.
        """
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", level=25, begin=BEGIN, expiration=END, deleted=0)
        db.session.add(coupon)
        db.session.commit()

        result = couponhelper.get_coupon_by_cid(coupon.cid + 2)
        self.assertEqual(result, None)

    def test_coupon_single(self):
        """
        Test getting a coupon, with a coupon in the database.
        """
        coupon = Coupon(rid=12, name="test", points=10, description="1$ off", level=25, begin=BEGIN, expiration=END, deleted=0)
        db.session.add(coupon)
        db.session.commit()

        result = couponhelper.get_coupon_by_cid(coupon.cid)
        self.assertEqual(result,
                            {"cid": coupon.cid,
                             "rid": coupon.rid,
                             "cname": coupon.name,
                             "cdescription": coupon.description,
                             "clevel": coupon.level,
                             "begin": coupon.begin,
                             "expiration": coupon.expiration,
                             "points": coupon.points,
                             "status": 1
                             })

    def test_coupon_none(self):
        """
        Test getting no coupon with no coupon in database.
        """
        result = couponhelper.get_coupon_by_cid(5)
        self.assertEqual(result, None)


if __name__ == "__main__":
    unittest.main()

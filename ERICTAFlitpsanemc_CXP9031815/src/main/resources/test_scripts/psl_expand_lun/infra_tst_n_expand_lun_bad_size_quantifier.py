#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/8881

:Requirement   ID: OSS-84540
:TestCaseID:   infra_tst_n_expand_lun_bad_size_quantifier
:Title:        Expand a storage pool LUN using the PSL
               where a invalid size quantifier is used
:Description:  Negative test case to expand a pool LUN using PSL
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Create a 1GB LUN on SAN
               2: Using the PSL expand the LUN to 5000gbb
               3: Verify the LUN could not be expanded
               4: Delete the expanded LUN
"""
from infra_utils.san_test import SanTest
from infra_utils.utils.san_utils import SanClient
import re


class TestCase(SanTest):

    """
    Test case to verify LUN expansion
    """
    

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        self.navi_target = self.mws
        self.san_client = SanClient(self.san, navi_target = self.navi_target)

        # 1)
        # Create a 1GB LUN on SAN
        # This LUN must not exist already in the SAN
        self.test_lun_name = ['infra_tst_n_expand__lun_oss84540']
        self.create_luns_for_testing(self.test_lun_name)
        


    def tearDown(self):
        """
        Clean up after the test case
        """
        # 4)
        # Delete the LUN created during the test
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Expand a pool LUN using the PSL
            1. Try and expand the LUN to 50gbb which is smaller than
               LUN that is created

        Actions:
            1: Assert exception is thrown
        """

        # 2)
        # Using the PSL try and expand the LUN to 500gbb
        res = self.san_client.sanapi_expand_pool_lun(self.test_lun_name[0], lun_size="500gbb")

        # 3)
        self.assertEqual(1, res.retcode)
        self.assertTrue(
            'SanApiOperationFailedException: Invalid size 500gbb'
            in res.stdout, "Error not found")

if __name__ == '__main__':
    TestCase().run_test()

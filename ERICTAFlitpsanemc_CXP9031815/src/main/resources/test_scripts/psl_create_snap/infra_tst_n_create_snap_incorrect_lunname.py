#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%2006

:Requirement   ID: OSS-77088
:TestCaseID:   infra_tst_n_create_snap_incorrect_lunname.py
:Title:        Create a snapshot of existing LUN with incorrect letter case
:Description:  Negative test case to create a snapshot of existing LUN with LUN 
               name of different letter case than the actual LUN name (use PSL)
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist 
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Assert the output contains errors
"""
from infra_utils.san_test import SanTest
from ptaf.utils.litp_cmd_utils import LitpUtils
from infra_utils.utils.san_utils import SanUtils

class TestCase(SanTest):

    def setUp(self):
        """
        Setup the test
        """
        super(TestCase, self).setUp()
        self.litp_utils = LitpUtils()
        self.sanapi_target = self.mws
        self.navi_target = self.mws
        
        # Create test lun. This lun must not exist already in the SAN
        self.snap_name="test_lun_oss77088_vandals1"
        self.test_lun_names = ['test_lun_oss77088']
        self.create_luns_for_testing(self.test_lun_names)

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Create a snapshot of existing LUN with LUN
        name of different letter case than the actual LUN name.
            1. Create a test LUN in a Storage Pool
        Actions:
            1: Assert that the output contains sufficient error message
        """
        # Create a snapshot of the test lun (PSL)
        cmd = self.sanapi_create_snapshot(self.snap_name, \
                                          self.test_lun_names[0].upper())
        self.assertTrue(cmd.retcode == 1)
        self.assertTrue("Exception" in cmd.stdout)

        # Use NAVI command to verify that the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

if __name__ == '__main__':
    TestCase().run_test()

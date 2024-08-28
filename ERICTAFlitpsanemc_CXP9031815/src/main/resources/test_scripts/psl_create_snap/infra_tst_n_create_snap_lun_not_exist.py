#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/INFRA:%20SAN%20Snapshot%2008

:Requirement   ID: OSS-77088
:TestCaseID:   infra_tst_n_create_snap_lun_not_exist.py
:Title:        Create a snapshot of a non-existent LUN name
:Description:  Negative test case to create snapshot of non-existent LUN name
:PreCondition: -
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
        
        self.test_lun_names = ['nowaythislunexists']
        self.snap_name="test_lun_oss77088_vandals1"
        luns = self.navi_get_luns()
        self.assertFalse(self.test_lun_names[0] in luns)

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Create a snapshot of non-existing LUN
        Actions:
            1: Assert the output contains sufficient error message
                when non-existing LUN is used
        """
        # Use NAVI command to verify that the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

        cmd = self.sanapi_create_snapshot(self.snap_name,self.test_lun_names[0])
        self.assertTrue(cmd.retcode == 1)
        self.assertTrue("Exception" in cmd.stdout)

        # Use NAVI command to verify that the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

if __name__ == '__main__':
    TestCase().run_test()

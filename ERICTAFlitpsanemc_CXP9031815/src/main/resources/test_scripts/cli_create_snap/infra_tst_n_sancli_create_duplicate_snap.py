#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/
    infra_tst_n_sancli_create_duplicate_snap
:Requirement   ID: OSS-77967
:TestCaseID:   infra_tst_n_sancli_create_duplicate_snap
:Title:        Create a snapshot using a duplicate snapshot name
:Description:  Negative test case to create snapshot using duplicate snap name
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Assert the output contains errors (sancli.py returns 1)
               2: Assert there is an explanatory error message logged
"""
from infra_utils.san_test import SanTest
from ptaf.utils.litp_cmd_utils import LitpUtils

class TestCase(SanTest):

    def setUp(self):
        """
        Setup the test
        """
        super(TestCase, self).setUp()
        self.sanapi_target = self.mws
        self.navi_target = self.mws

        # Create test lun. This lun must not exist in the SAN
        self.snap_name="test_lun_oss77967_vandals1"
        self.test_lun_names = ['test_lun_oss77967']
        self.create_luns_for_testing(self.test_lun_names)

        # Use NAVI command to verify that the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

        # Create a snapshot of the test lun (CLI)
        cmd = self.sancli_create_snapshot(self.snap_name,self.test_lun_names[0])
        self.assertTrue(cmd.retcode == 0)

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Create a snapshot using a duplicate snapshot name on same LUN
            1. Create a test LUN in a Storage Pool
            2. Create a snap shot on same lun using the same name as in setup()
        Actions:
            1: Assert the output contains errors
            2: Assert the output contains sufficient error message
                when a duplicate snapshot name on same LUN is attempted
        """
        # Use NAVI command to verify that the snapshot exists
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 0)

        # Create a snapshot of the same test lun using the same snap_name (CLI)
        cmd = self.sancli_create_snapshot(self.snap_name,self.test_lun_names[0])
        self.assertTrue(cmd.retcode == 1)
        self.assertTrue("snapshot name is already in use" in cmd.stdout)

if __name__ == '__main__':
    TestCase().run_test()

#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/infra_tst_p_sancli_create_snap

:Requirement   ID: OSS-77967
:TestCaseID:   infra_tst_p_sancli_create_snap
:Title:        Create snapshot of existing LUN with LUN name (using SAN CLI)
:Description:  Positive test case to create snapshot of existing LUN
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Assert the output contains no errors (sancli.py returns 0)
               2: Assert the snap shot was created with correct name
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

        # Create test lun. This lun must not exist already in the SAN
        self.snap_name="test_lun_oss77967_vandals1"
        self.test_lun_names = ['test_lun_oss77967']
        self.create_luns_for_testing(self.test_lun_names)

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Create snapshot of existing LUN
            1. Using sancli.py, create a snapshot of the test LUN
        Actions:
            1: Assert the output contains no errors
            2: Assert the snap shot was created with correct name
        """
        # Use NAVI command to verify the snapshot does not exist
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 1)

        # Create a snapshot of the test lun (CLI)
        cmd = self.sancli_create_snapshot(self.snap_name, self.test_lun_names[0])
        self.assertTrue(cmd.retcode == 0)
        trace_message = "snapshot name:test_lun_oss77967_vandals1 returned"
        self.assertTrue(trace_message in cmd.stdout)

        # Use NAVI command to verify that the snapshot exists
        list = self.navi_list_one_snap(self.snap_name)
        self.assertTrue(list.retcode == 0)

if __name__ == '__main__':
    TestCase().run_test()

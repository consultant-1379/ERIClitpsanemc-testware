#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/infra_tst_p_sancli_create_second_snap

:Requirement   ID: OSS-77967
:TestCaseID:   infra_tst_p_sancli_create_second_snap
:Title:        Create a snapshot of a LUN which already has a snap-shot
:Description:  Positive test case to create a snapshot of a LUN which already
               has a snap-shot
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
        self.snap_names = ["vandals1","vandals2"]
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
        Create a snapshot of a LUN which already has a snap-shot
            1. Create a snap shot then create a second snap shot
        Actions:
            1: Assert the output contains no errors
        """

        # Use NAVI command to verify that the snapshots do not exist
        for snaps in self.snap_names:
            list = self.navi_list_one_snap(snaps)
            self.assertTrue(list.retcode == 1)

        # Create snapshots of the test lun (CLI)
        for testlun in self.test_lun_names:
            for snap in self.snap_names:
                snap = testlun + '_' + snap
                cmd = self.sancli_create_snapshot(snap, testlun)
                self.assertTrue(cmd.retcode == 0)
                trace_message = "snapshot name:" + snap + " returned"
                self.assertTrue(trace_message in cmd.stdout)

        # Use NAVI command to verify that the snapshots exists
        for snaps in self.snap_names:
            list = self.navi_list_one_snap(snaps)
            self.assertTrue(list.retcode == 0)

if __name__ == '__main__':
    TestCase().run_test()

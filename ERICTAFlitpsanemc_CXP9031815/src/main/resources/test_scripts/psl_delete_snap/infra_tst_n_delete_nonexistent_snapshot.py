#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/infra_tst_n_delete_nonexistent_snapshot

:Requirement   ID: OSS-70299
:TestCaseID:   infra_tst_n_delete_nonexistent_snapshot
:Title:        Try to delete a nonexistent snapshot using PSL
:Description:  Negative test case to try to delete a nonexistent snapshot using
               PSL
:PreCondition: Create a test LUN in a Storage Pool. This LUN must not exist
               already in the SAN
:Type:         Functional test case
:TestStep:     1: Create a 1GB LUN on SAN
               1.1: execute infra_is_1GB_LUN_Created.py
               2: Try to delete a nonexistent snapshot on the LUN
               2.1: Verify the output contains a sufficient error message
               3: Delete the LUN created during the test

Verify that deletion of a snapshot which doesn't exist returns an appropriate
error.
"""

from infra_utils.san_test import SanTest

class TestCase(SanTest):

    """
    Test case to verify LUNs defined in the model
    """

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        self.sanapi_target = self.mws
        self.navi_target = self.mws

        self.test_lun_name = 'vandals_test_delete_nonexist_snap_lun_oss77090'

        self.snap_name = [
                'snapshot_to_auto_test_failed_snapshot_deletion_nonexisting']

        # 1) Create a 1GB LUN on SAN
        self.create_luns_for_testing([self.test_lun_name])

    def tearDown(self):
        """
        Clean up after the test case
        """

        # 3: Delete the LUN created during the test
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Test case implementation
        Try to delete a nonexistent snapshot using PSL
            1. Create a 1GB LUN on SAN
            2. Try to delete a nonexistent snapshot on the LUN

        Actions:
            1: Verify that the output contains a sufficient error message
        """
        # 2) Try to delete a nonexistent snapshot on the LUN
        cmd = self.sanapi_delete_snapshot(self.snap_name[0])
        self.assertTrue(cmd.retcode != 0,
                        'Fail: snapshot exists')

        # Check that appropriate exception text is output
        exception_message = 'Cannot destroy the snapshot. The specified'
        exception_message += ' snapshot does not exist.'
        self.assertTrue(exception_message in cmd.stdout,
                        'Fail: expected Exception not found')

if __name__ == '__main__':
    TestCase().run_test()

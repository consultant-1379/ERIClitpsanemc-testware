#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/infra_tst_n_restore_snap_lun_not_exist

:Jira          Story OSS-77089
:Requirement   ID: OSS-77089
:TestCaseID    infra_tst_n_restore_snap_lun_not_exist.py
:Title         Try to restore a snapshot on a non-existent LUN using PSL
:Description   Negative test case to try to restore a snapshot on a
               non-existent LUN using PSL
:PreCondition  -
:Type          Functional test case
:TestStep      1: Assert the output contains sufficient error message
"""
from infra_utils.san_test import SanTest

class TestCase(SanTest):

    def setUp(self):
        """
        Set up the test case
        """
        super(TestCase, self).setUp()
        self.sanapi_target = self.mws
        self.navi_target = self.mws
        self.test_lun_name = 'test_lun_oss77089'
        self.create_luns_for_testing([self.test_lun_name])
        self.snap_name = "test_lun_oss77089_snap"

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Try to restore snapshots of a LUN which does not exist on the SAN

        Actions:
            1: Assert the output contains sufficient error message
               when non-existing LUN is used
        """

        # Create snapshot
        cmd = self.sanapi_create_snapshot(self.snap_name, self.test_lun_name)
        self.assertTrue(cmd.retcode == 0)

        # Try to restore the snapshot but use incorrect LUN name
        cmd = self.sanapi_restore_snapshot(self.snap_name, self.test_lun_name.upper())

        # Check that restore_snapshot failed
        self.assertTrue(cmd.retcode != 0,
                        'Fail: restore_snapshot successful with wrong LUN name')

        # Check that appropriate exception text is output
        exception_message = 'Could not retrieve the specified (pool lun).'
        exception_message += ' The (pool lun) may not exist'
        self.assertTrue(exception_message in cmd.stdout,
                        'Fail: expected Exception not found')

if __name__ == '__main__':
    TestCase().run_test()

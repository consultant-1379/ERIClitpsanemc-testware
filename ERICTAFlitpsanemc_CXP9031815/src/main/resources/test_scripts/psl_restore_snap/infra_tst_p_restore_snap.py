#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/infra_tst_p_restore_snap

:Jira          Story OSS-77089
:Requirement   ID: OSS-77089
:TestCaseID    infra_tst_p_restore_snap.py
:Title         Create two LUN snapshots and verify they both can be restored
               using PSL
:Description   The test creates two LUN snapshots and restores each of them
:PreCondition  The LUN used in this test case doesn't exist on the SAN
:Type          Functional test case
:TestStep      1: Assert the output contains no errors
               2: Assert the snap shot was restored
"""
from infra_utils.san_test import SanTest
from re import search

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
        self.snap_names = ("test_lun_oss77089_snap1", "test_lun_oss77089_snap2")

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Restore snapshots of existing LUN
            1. Create two snapshots of the test LUN
            2. Restore the first snapshot
            3. Restore the second snapshot

        Actions:
            1: Assert that the output contains no errors
            2: Assert that the snapshots still exist after restore
            3: Assert that the backup snapshots were deleted
        """

        # Create snapshots on the LUN using PSL create_snapshot
        for snap in self.snap_names:
            cmd = self.sanapi_create_snapshot(snap, self.test_lun_name)
            self.assertTrue(cmd.retcode == 0,
                            'Fail: create_snapshot failed')

        # Restore snapshots using PSL restore_snapshot
        for snap in self.snap_names:
            cmd = self.sanapi_restore_snapshot(snap, self.test_lun_name)
            self.assertTrue(cmd.retcode == 0,
                            'Fail: restore_snapshot failed')

            # Check that PSL restore_snapshot returned True
            self.assertTrue(search('True', cmd.stdout.splitlines()[-1]),
                            'Fail: restore_snapshot did not return True')

            # Check that LUN state is Ready after restore snapshot
            lun_info = self.navi_get_lun(self.test_lun_name)
            self.assertEqual(lun_info['Current State'], 'Ready',
                             'Fail: LUN state not Ready after restore_snapshot')

            snaps_dict = self.sanapi_list_snapshots_one_lun(self.test_lun_name)
            # Check that backup snapshot has been deleted
            self.assertEqual(len(snaps_dict), 2,
                             'Fail: Unexpected number of snapshots for LUN')

            # Check that snapshot still exists after restore
            self.assertTrue(snap in snaps_dict,
                            'Fail: Restored snapshot not found')

if __name__ == '__main__':
    TestCase().run_test()

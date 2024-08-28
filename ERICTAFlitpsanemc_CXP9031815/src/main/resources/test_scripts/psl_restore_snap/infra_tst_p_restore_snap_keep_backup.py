#!/usr/bin/env python

"""
TEST CASE DESCRIPTION:
http://taftm.lmera.ericsson.se/#tm/viewTC/infra_tst_p_restore_snap_keep_backup

:Jira          Story OSS-77089
:Requirement   ID: OSS-77089
:TestCaseID:   infra_tst_p_restore_snap_keep_backup.py
:Title:        Restore a snapshot using PSL with flag delete_backup=False and
               make sure the backup snapshot exists and can be restored
:Description:  Positive test case to restore a snapshot using PSL with flag
               delete_backup=False and make sure the backup snapshot exists and
               can be restored
:PreCondition: The LUN used in this test case doesn't already exist on the SAN
:Type:         Functional test case
:TestStep:     1: Assert the output contains no errors
               2: Assert the backup snap shot can be restored
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
        self.snap_name = "test_lun_oss77089_snap"
        self.backup_snap_name = '_'.join(['restore', self.snap_name])

    def tearDown(self):
        """
        Clean up after the test case
        """
        self.delete_luns_for_testing()
        super(TestCase, self).tearDown()

    def test(self):
        """
        Restore snapshots of existing LUN
            1. Create a snapshot of the test LUN
            2. Restore the snapshot with flag delete_backup=False

        Actions:
            1: Assert that the output contains no errors
            2: Assert that the snapshots still exist
            3: Assert that the backup snapshots exists
        """

        # Create a snapshot on the LUN using PSL create_snapshot
        cmd = self.sanapi_create_snapshot(self.snap_name, self.test_lun_name)
        self.assertTrue(cmd.retcode == 0,
                        'Fail: create_snapshot failed')

        # Restore the snapshot using PSL restore_snapshot with
        # flag delete_backup=False
        cmd = self.sanapi_restore_snapshot(self.snap_name,
                                           self.test_lun_name, 'no')
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
        # Check that snapshot still exists after restore
        self.assertTrue(self.snap_name in snaps_dict,
                            'Fail: Restored snapshot not found')

        # Check that the backup snapshot exists
        self.assertTrue(self.backup_snap_name in snaps_dict,
                            'Fail: Backup snapshot not found')

if __name__ == '__main__':
    TestCase().run_test()
